# pylint: disable=C0111, C0301
import os
import sys
import appdirs

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

if sys.version_info[0] < 3:
    STRING_TYPE = basestring
else:
    STRING_TYPE = str


class TestDarwin(unittest.TestCase):
    def setUp(self):
        appdirs.system = 'darwin'
        os.environ['USER'] = "travis"
        os.environ['HOME'] = "/Users/travis"

    def test_wrapper(self):
        dirs = appdirs.AppDirs('MyApp', 'MyCompany', version=1.0)
        self.assertEqual(dirs.user_data_dir, "/Users/travis/Library/Application Support/MyCompany/MyApp/1.0")
        self.assertEqual(dirs.site_data_dir, "/Library/Application Support/MyCompany/MyApp/1.0")
        self.assertEqual(dirs.user_config_dir, "/Users/travis/Library/Preferences/MyCompany/MyApp/1.0")
        self.assertEqual(dirs.site_config_dir, "/Library/Preferences/MyCompany/MyApp/1.0")
        self.assertEqual(dirs.user_cache_dir, "/Users/travis/Library/Caches/MyCompany/MyApp/1.0")
        self.assertEqual(dirs.user_state_dir, "/Users/travis/Library/Application Support/MyCompany/MyApp/1.0")
        self.assertEqual(dirs.user_log_dir, "/Users/travis/Library/Logs/MyCompany/MyApp/1.0")

    def test_program_dirs(self):
        self.assertEqual(
            appdirs.user_data_dir('MyApp', 'MyCompany', 1.0), "/Users/travis/Library/Application Support/MyCompany/MyApp/1.0")
        self.assertEqual(
            appdirs.site_data_dir('MyApp', 'MyCompany', 1.0), "/Library/Application Support/MyCompany/MyApp/1.0")
        self.assertEqual(
            appdirs.user_config_dir('MyApp', 'MyCompany', 1.0), "/Users/travis/Library/Preferences/MyCompany/MyApp/1.0")
        self.assertEqual(
            appdirs.site_config_dir('MyApp', 'MyCompany', 1.0), "/Library/Preferences/MyCompany/MyApp/1.0")
        self.assertEqual(
            appdirs.user_cache_dir('MyApp', 'MyCompany', 1.0), "/Users/travis/Library/Caches/MyCompany/MyApp/1.0")
        self.assertEqual(
            appdirs.user_state_dir('MyApp', 'MyCompany', 1.0), "/Users/travis/Library/Application Support/MyCompany/MyApp/1.0")
        self.assertEqual(
            appdirs.user_log_dir('MyApp', 'MyCompany', 1.0), "/Users/travis/Library/Logs/MyCompany/MyApp/1.0")


class TestAppDir(unittest.TestCase):
    def test_metadata(self):
        self.assertTrue(hasattr(appdirs, "__version__"))
        self.assertTrue(hasattr(appdirs, "__version_info__"))

if __name__ == "__main__":
    print("Starting tests")
    unittest.main()
