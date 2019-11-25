import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
    '..')))
from facebook_snooper import Session
from mock import MockBrowserWrapper 


class TestSession(unittest.TestCase):
    def setUp(self):
        self.session = Session(MockBrowserWrapper())
    
    def test_log_in(self):
        self.log_in()
        self.assertTrue(self.session.connected)

    def test_search(self):
        self.log_in()
        results = self.session.search('test not used')
        self.assertTrue(results)

    def test_profile(self):
        self.log_in()
        name, image_link, info = self.session.profile_info('not.used.id')
        self.assertNotEqual(name, '')
        self.assertNotEqual(image_link, '')
        self.assertTrue(info)

    def log_in(self):
        self.session.log_in('test@notused', 'not_password')


if __name__ == '__main__':
    unittest.main()