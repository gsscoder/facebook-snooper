"""
before running tests you need to create 'test-data' folder:
$ cd facebook_snooper
$ mkdir test-data
and populate it (choose a profile with at least one introductory item)
$ python3
>>> from facebook_snooper import _test_save_html, _get_intro_html
>>> from facebook_snooper import log_in, _get_search_html
>>> log_in('user@email.com', 'user_password')
True
>>> _test_save_html('profile', _get_intro_html('fb.profile.id'))
>>> _test_save_html('search', _get_search_html('your query'))
"""


from facebook_snooper import _test_load_html, _extract_intro, \
                             _extract_profiles, log_in
import unittest


# Set only_local to True to skip tests that connects to Facebook
only_local = False


class TestExtractIntro(unittest.TestCase):
    
    def test_extract_intro(self):
        html = _test_load_html('profile')
        items = _extract_intro(html)

        self.assertGreater(len(items), 0)


class TestExtractProfiles(unittest.TestCase):

    def test_extract_profiles(self):
        html = _test_load_html('search')
        profiles = _extract_profiles(html)

        self.assertGreater(len(profiles), 0)


class TestLogIn(unittest.TestCase):

    def test_bad_login(self):
        if not only_local:
            self.assertFalse(log_in('invalid','login'))


if __name__ == '__main__':
    unittest.main()