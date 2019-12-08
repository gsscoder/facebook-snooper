import os.path
from abc import abstractmethod
from mechanicalsoup import StatefulBrowser

from .exceptions import LogInError, NotConnectedError
from .wrapper import BrowserWrapper
from ._parser import parse_image, parse_info, parse_search


__all__ = [
    "Session"
]


class Session:
    BASE_URL = 'https://m.facebook.com'

    def __init__(self, browser_wrapper):
        self._connected = False
        self._current_html = None
        self._browser_wrapper = browser_wrapper
        self._browser = StatefulBrowser()
        self._browser.addHeaders = [
                ('User-Agent', 'Firefox'),
                ('Accept-Language', 'en-US,en;q=0.5')
                ]

    def __del__(self):
        self._dispose()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._dispose()

    @property
    def connected(self):
        return self._connected

    def log_in(self, username, password):
        try:
            # Log in to non-mobile site is more reliable
            self._browser_wrapper.open(self._browser, 'https://www.facebook.com')
            self._browser.select_form('form[id="login_form"]')
            self._browser['email'] = username
            self._browser['pass'] =  password        
            self._browser_wrapper.submit_selected(self._browser)
            # Check if we really are in account profile page
            if self._browser.get_current_page().find('form',
                action='/search/top/'):
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
            self._browser_wrapper.open(self._browser, f'{Session.BASE_URL}/{id_}')
            name  = self._sanitize_title(
                self._browser.get_current_page().find('title').text)
            image = parse_image(self._browser.get_current_page(), name)
            info = parse_info(self._browser.get_current_page())
            return name, image, info
        except:
            return None

    def search(self, query):
        """
        Execute search of a given text returning a tuple with ID,
        descriptions and URI.
        """
        url_query = '+'.join(query.split())
        url_path = f'/search/top/?q={url_query}' \
            if self._connected else f'/public/{url_query}'
        try:
            self._browser_wrapper.open(self._browser,
                f'{Session.BASE_URL}{url_path}{url_query}')
            return parse_search(self._browser.get_current_page(),
                Session.BASE_URL)
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