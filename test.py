"""
before running tests you need to create 'test-data' folder:
$ cd facebook_snooper
$ mkdir test-data
and populate it (choose a profile with at least one introductory item)
$ python3
>>> from facebook_snooper import _test_save_html,
    _get_intro_html, log_in
>>> log_in('user@email.com', 'user_password')
True
>>> _test_save_html('profile', _get_intro_html('fb.profile.id'))
"""

import unittest
from facebook_snooper import _test_load_html, _extract_intro, \
                             log_in

class TestExtractIntro(unittest.TestCase):
    
    def test_extract_intro(self):
        html = _test_load_html('profile')
        items = _extract_intro(html)

        self.assertGreater(len(items), 0)


class TestLogIn(unittest.TestCase):

    def test_bad_login(self):
        self.assertFalse(log_in('invalid','login'))


if __name__ == '__main__':
    unittest.main()