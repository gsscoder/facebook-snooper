import os.path
from abc import abstractmethod
from mechanicalsoup import StatefulBrowser
from .exceptions import LogInError, NotConnectedError
from ._parser import parse_image, parse_info, parse_search


__all__ = [
    "Session"
]


class Session:
    BASE_URL = 'https://m.facebook.com'

    def __init__(self):
        self._connected = False
        self._current_html = None
        self._browser = StatefulBrowser()
        self._browser.addHeaders = [
                ('User-Agent', 'Mozilla/5.0 (Linux; Android 7.0; PLUS ' +
                'Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                'Chrome/61.0.3163.98 Mobile Safari/537.36'), \
                ('Accept-Language', 'en-US,en;q=0.5')
                ]

    def __del__(self):
        self._dispose()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._dispose()

    def log_in(self, username, password):
        try:
            self._browser.open(Session.BASE_URL)
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
            self._connected = False

    def profile_info(self, id_):
        """Retrieve informations for a given profile."""
        self._ensure_connected()
        try:
            self._browser.open(f'{Session.BASE_URL}/{id_}')
            name  = self._sanitize_title(
                self._browser.get_current_page().find('title').text)
            image = parse_image(name, self._browser.get_current_page())
            info = parse_info(self._browser.get_current_page())
            return name, image, info
        except:
            return None

    def search(self, query):
        """
        Execute search of a given text returning a tuple with ID,
        descriptions and URI.
        """
        self._ensure_connected()
        try:
            url_query = '+'.join(query.split())
            self._browser.open(f'{Session.BASE_URL}/search/top/?q={url_query}')
            return parse_search(self._browser.get_current_page())
        except:
            return None

    def _ensure_connected(self):
        if not self._connected:
            raise NotConnectedError('No active connection or required login')

    def _sanitize_title(self, title):
        # Handle cases like 'Some One - Home'
        if '-' in title:
            return title.split('-')[0].strip()
        return title

    def _dispose(self):
        if self._connected:
            self.log_out()