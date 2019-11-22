import os.path
from abc import abstractmethod
from mechanicalsoup import StatefulBrowser, \
                           LinkNotFoundError
from ._parser import Parser


__all__ = [
    "Session",
    "FacebookSession"
]


class LogInError(Exception):
    pass


class NotConnectedError(Exception):
    pass


class Session:
    def __init__(self):
        self._connected = False
        self._current_html = None
        self._parser = Parser()

    def __del__(self):
        self._dispose()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._dispose()

    def _dispose(self):
        if self.connected:
            self.log_out()

    @property
    def current_html(self):
        """Current page HTML for testing purposes."""
        return self._current_html

    @property
    def connected(self):
        return self._connected

    @abstractmethod
    def log_in(self, username, password):
        """Log in to Facebook with username and password."""
        pass

    @abstractmethod
    def log_out(self):
        pass

    def profile_info(self, profile_id):
        """Retrieve informations for a given profile."""
        self._ensure_connected()
        try:
            profile_html = self._get_profile_html(profile_id)
            name  = self._sanitize_title(self._get_current_title())
            image = self._parser.parse_image(profile_html)
            intro =  self._parser.parse_intro(profile_html)
            followers = self._parser.parse_followers(profile_html)
            return name, image, followers, intro
        except:
            return None

    def search(self, query):
        """Execute search of a given text returning a tuple with ID, description and URI."""
        self._ensure_connected()
        try:
            return self._parser.parse_search_result(self._get_search_html(query))
        except:
            return None

    @abstractmethod
    def _get_current_title(self):
        pass

    @abstractmethod
    def _get_profile_html(self, profile_id):
        pass

    @abstractmethod
    def _get_search_html(self, query):
        pass

    def _ensure_connected(self):
        if not self._connected:
            raise NotConnectedError("No active connection or valid login")

    def _sanitize_title(self, title):
        # Handle cases like 'Some One - Home'
        if '-' in title:
            return title.split('-')[0].strip()
        return title


class FacebookSession(Session):
    def log_in(self, username, password):
        self._base_url = 'https://www.facebook.com'
        try:
            self._browser = StatefulBrowser()
            self._browser.addHeaders = [
                    ('User-Agent', 'Firefox'), \
                    ('Accept-Language', 'en-US,en;q=0.5')
                    ]
            self._browser.open(self._base_url)
            self._current_html = str(self._browser.get_current_page())
            self._browser.select_form('form[id="login_form"]')
            self._browser['email'] = username
            self._browser['pass'] =  password        
            self._browser.submit_selected()
            self._browser.select_form('form[action="/search/top/"]')
            self._connected = True
        except:
            raise LogInError("Unable to log in as {username}")
        return self

    def log_out(self):
        if self._connected:
            self._browser.close()
            self._browser = None
            self._connected = False

    def _get_current_title(self):
        return self._browser.get_current_page().find('title').text

    def _get_profile_html(self, profile_id):
        url = f'{self._base_url}/{profile_id}'
        self._browser.open(url)
        self._current_html = str(self._browser.get_current_page())
        return self._current_html

    def _get_search_html(self, query):
        self._browser.select_form('form[action="/search/top/"]')
        self._browser['q'] = query
        self._browser.submit_selected()
        self._current_html = str(self._browser.get_current_page())
        return self._current_html