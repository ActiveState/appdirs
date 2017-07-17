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


class TestWindows(unittest.TestCase):
    def setUp(self):
        os.environ['APPDATA'] = "C:\\Users\\appveyor\\AppData\\Roaming"
        os.environ['ALLUSERSPROFILE'] = "C:\\ProgramData"
        appdirs.system = 'win32'

    def test_wrapper_without_roaming(self):
        dirs = appdirs.AppDirs('MyApp', 'MyCompany', version=1.0, roaming=False)
        self.assertEqual(dirs.user_data_dir, "C:\\Users\\appveyor\\AppData\\Local\\MyCompany\\MyApp\\1.0")
        self.assertEqual(dirs.site_data_dir, "C:\\ProgramData\\MyCompany\\MyApp\\1.0")
        self.assertEqual(dirs.user_config_dir, "C:\\Users\\appveyor\\AppData\\Local\\MyCompany\\MyApp\\1.0")
        self.assertEqual(dirs.site_config_dir, "C:\\ProgramData\\MyCompany\\MyApp\\1.0")
        self.assertEqual(dirs.user_cache_dir, "C:\\Users\\appveyor\\AppData\\Local\\MyCompany\\MyApp\\Cache\\1.0")
        self.assertEqual(dirs.user_state_dir, "C:\\Users\\appveyor\\AppData\\Local\\MyCompany\\MyApp\\1.0")
        self.assertEqual(dirs.user_log_dir, "C:\\Users\\appveyor\\AppData\\Local\\MyCompany\\MyApp\\1.0\\Logs")

    def test_wrapper_with_roaming(self):
        dirs = appdirs.AppDirs('MyApp', 'MyCompany', version=1.0, roaming=True)
        self.assertEqual(dirs.user_data_dir, "C:\\Users\\appveyor\\AppData\\Roaming\\MyCompany\\MyApp\\1.0")
        self.assertEqual(dirs.site_data_dir, "C:\\ProgramData\\MyCompany\\MyApp\\1.0")
        self.assertEqual(dirs.user_config_dir, "C:\\Users\\appveyor\\AppData\\Roaming\\MyCompany\\MyApp\\1.0")
        self.assertEqual(dirs.site_config_dir, "C:\\ProgramData\\MyCompany\\MyApp\\1.0")
        self.assertEqual(dirs.user_cache_dir, "C:\\Users\\appveyor\\AppData\\Local\\MyCompany\\MyApp\\Cache\\1.0")
        self.assertEqual(dirs.user_state_dir, "C:\\Users\\appveyor\\AppData\\Local\\MyCompany\\MyApp\\1.0")
        self.assertEqual(dirs.user_log_dir, "C:\\Users\\appveyor\\AppData\\Local\\MyCompany\\MyApp\\1.0\\Logs")

    def test_program_dirs(self):
        self.assertEqual(
            appdirs.user_data_dir('MyApp', 'MyCompany', 1.0, False), "C:\\Users\\appveyor\\AppData\\Local\\MyCompany\\MyApp\\1.0")
        self.assertEqual(
            appdirs.user_data_dir('MyApp', 'MyCompany', 1.0, True), "C:\\Users\\appveyor\\AppData\\Roaming\\MyCompany\\MyApp\\1.0")
        self.assertEqual(
            appdirs.site_data_dir('MyApp', 'MyCompany', 1.0), "C:\\ProgramData\\MyCompany\\MyApp\\1.0")
        self.assertEqual(
            appdirs.user_config_dir('MyApp', 'MyCompany', 1.0, False), "C:\\Users\\appveyor\\AppData\\Local\\MyCompany\\MyApp\\1.0")
        self.assertEqual(
            appdirs.user_config_dir('MyApp', 'MyCompany', 1.0, True), "C:\\Users\\appveyor\\AppData\\Roaming\\MyCompany\\MyApp\\1.0")
        self.assertEqual(
            appdirs.site_config_dir('MyApp', 'MyCompany', 1.0), "C:\\ProgramData\\MyCompany\\MyApp\\1.0")
        self.assertEqual(
            appdirs.user_cache_dir('MyApp', 'MyCompany', 1.0), "C:\\Users\\appveyor\\AppData\\Local\\MyCompany\\MyApp\\Cache\\1.0")
        self.assertEqual(
            appdirs.user_state_dir('MyApp', 'MyCompany', 1.0), "C:\\Users\\appveyor\\AppData\\Local\\MyCompany\\MyApp\\1.0")
        self.assertEqual(
            appdirs.user_log_dir('MyApp', 'MyCompany', 1.0), "C:\\Users\\appveyor\\AppData\\Local\\MyCompany\\MyApp\\1.0\\Logs")

    def tearDown(self):
        del os.environ['APPDATA']
        del os.environ['ALLUSERSPROFILE']


class TestAppDir(unittest.TestCase):
    def test_metadata(self):
        self.assertTrue(hasattr(appdirs, "__version__"))
        self.assertTrue(hasattr(appdirs, "__version_info__"))

if __name__ == "__main__":
    print("Starting tests")
    unittest.main()
