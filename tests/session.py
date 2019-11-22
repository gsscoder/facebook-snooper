"""
before running tests you need to create 'test-data' folder,
please see README.md
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from facebook_snooper import Session
from mock import MockSession


class SessionTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(SessionTestCase, self).__init__(*args, **kwargs)
        self._mock_session : Session =  MockSession()

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