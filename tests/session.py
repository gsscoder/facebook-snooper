"""
before running tests you need to create 'test-data' folder,
please see README.md
"""


import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from facebook_snooper import Session


class MockSession(Session):
    def __init__(self):
        super()
        self._connected = False
        self.pages_dir = os.path.join('.', 'tests/pages')

    def _load_html(self, filename):
        with open(os.path.join(self.pages_dir, f'{filename}.html'), 'r') as f:
            return f.read() 
    
    def _get_current_title(self):
        return "someone"

    def _get_profile_html(self, profile_id):
        return self._load_html('profile')

    def _get_search_html(self, query):
        return self._load_html('search')

    def log_in(self, username, password):
        self._connected = True
        return self


class SessionTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(SessionTestCase, self).__init__(*args, **kwargs)
        self._mock_session =  MockSession()

    @property
    def mock_session(self):
        return self._mock_session

class TestGetIntro(SessionTestCase):
    def test_profile_info(self):
        profile = self.mock_session.profile_info('test')
        self.assertIsNotNone(profile)
        name, image_link, followers, intro = profile
        self.assertGreater(len(name), 0)
        self.assertGreater(len(image_link), 0)
        self.assertGreater(len(followers), 0)
        self.assertGreater(len(intro), 0)


class TestSearch(SessionTestCase):
    def test_search_profiles(self):
        results = self.mock_session.search('test')
        self.assertGreater(len(results), 0)


if __name__ == '__main__':
    unittest.main()