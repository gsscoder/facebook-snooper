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


mock_session : Session = MockSession()


class TestGetIntro(unittest.TestCase):
    def test_profile_info(self):
        profile = mock_session.profile_info('test')
        self.assertIsNotNone(profile)
        name, image_link, followers, intro = profile
        self.assertGreater(len(name), 0)
        self.assertGreater(len(image_link), 0)
        self.assertGreater(len(followers), 0)
        self.assertGreater(len(intro), 0)


class TestSearch(unittest.TestCase):
    def test_search_profiles(self):
        results = mock_session.search('test')
        self.assertGreater(len(results), 0)


if __name__ == '__main__':
    unittest.main()