import os
from facebook_snooper import Session


class MockSession(Session):
    def __init__(self):
        super()
        self._connected = True
        self.pages_dir = os.path.join('.', 'tests/pages')

    def _load_html(self, filename):
        with open(os.path.join(self.pages_dir, f'{filename}.html'), 'r') as f:
            return f.read() 
    
    def _get_intro_html(self, profile_id):
        return self._load_html('profile')

    def _get_search_html(self, query):
        return self._load_html('search')

    def log_in(self, username, password):
        return self._connected