import os.path
from abc import abstractmethod
from mechanicalsoup import StatefulBrowser, \
                           LinkNotFoundError
from .exceptions import LogInError, NotConnectedError
from ._parser import Parser


__all__ = [
    "Session"
]


class Session:
    BASE_URL = 'https://m.facebook.com'

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

    def log_in(self, username, password):
        try:
            self._browser = StatefulBrowser()
            self._browser.addHeaders = [
                    ('User-Agent', 'Mozilla/5.0 (Linux; Android 7.0; ' + \
                        'PLUS Build/NRD90M) AppleWebKit/537.36 (KHTML, ' + \
                        'like Gecko) Chrome/61.0.3163.98 Mobile ' + \
                        'Safari/537.36'), \
                    ('Accept-Language', 'en-US,en;q=0.5')
                    ]
            self._browser.open(Session.BASE_URL)
            self._current_html = str(self._browser.get_current_page())
            self._browser.select_form('form[id="login_form"]')
            self._browser['email'] = username
            self._browser['pass'] =  password        
            self._browser.submit_selected()
            self._connected = True
        except:
            raise LogInError(f'Unable to log in as {username}')
        return self

    def log_out(self):
        if self._connected:
            self._browser.close()
            self._browser = None
            self._connected = False


    def profile_info(self, id_):
        """Retrieve informations for a given profile."""
        self._ensure_connected()
        try:
            profile_html = self._get_profile_html(id_)
            name  = self._sanitize_title(self._get_current_title())
            image = self._parser.parse_image(name, self._get_current_soup())
            info = self._parser.parse_info(self._get_current_soup())
            return name, image, info
        except:
            return None

    def search(self, query):
        """Execute search of a given text returning a tuple with ID, description and URI."""
        self._ensure_connected()
        try:
            return self._parser.parse_search_result(self._get_search_soup(query))
        except:
            return None

    def _get_current_title(self):
        return self._browser.get_current_page().find('title').text

    def _get_profile_html(self, profile_id):
        url = f'{Session.BASE_URL}/{profile_id}'
        self._browser.open(url)
        self._current_html = str(self._browser.get_current_page())
        return self._current_html

    def _get_search_soup(self, query):
        url_query = '+'.join(query.split())
        self._browser.open(f'{Session.BASE_URL}/search/top/?q={url_query}')
        self._current_html = str(self._browser.get_current_page())
        return self._browser.get_current_page()

    def _get_current_soup(self):
        return self._browser.get_current_page()

    def _ensure_connected(self):
        if not self._connected:
            raise NotConnectedError('No active connection or valid login')

    def _sanitize_title(self, title):
        # Handle cases like 'Some One - Home'
        if '-' in title:
            return title.split('-')[0].strip()
        return title