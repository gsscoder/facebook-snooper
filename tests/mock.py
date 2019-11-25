import os
from facebook_snooper import BrowserWrapper


class MockBrowserWrapper(BrowserWrapper):
    def __init__(self):
        self._pages_dir = os.path.join('.', 'tests', 'pages')
        self._in_login = False

    def open(self, browser, url):
        if url == 'https://www.facebook.com':
            self._in_login = True
            self._open_from_disk(browser, 'login')
        elif url.startswith('https://m.facebook.com/search/top/?q='):
            self._open_from_disk(browser, 'search')
        elif url.startswith('https://m.facebook.com/'):
            self._open_from_disk(browser, 'profile')      

    def submit_selected(self, browser):
        if self._in_login:
            self._open_from_disk(browser, 'logged')
            self._in_login = False

    def _open_from_disk(self, browser, filename):
        with open(os.path.join(self._pages_dir, f'{filename}.html')) as page:
            browser.open_fake_page(page.read())