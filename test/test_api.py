import sys
import unittest
import appdirs

if sys.version_info[0] < 3:
    STRING_TYPE = basestring
    PATH_TYPE = basestring
elif sys.version_info[0] == 3 and sys.version_info[1] < 4:
    STRING_TYPE = str
    PATH_TYPE = str
else:
    import pathlib
    STRING_TYPE = str
    PATH_TYPE = pathlib.Path


class Test_AppDir(unittest.TestCase):
    def test_metadata(self):
        self.assertTrue(hasattr(appdirs, "__version__"))
        self.assertTrue(hasattr(appdirs, "__version_info__"))

    def test_helpers(self):
        self.assertIsInstance(
            appdirs.user_data_dir('MyApp', 'MyCompany'), STRING_TYPE)
        self.assertIsInstance(
            appdirs.site_data_dir('MyApp', 'MyCompany'), STRING_TYPE)
        self.assertIsInstance(
            appdirs.user_cache_dir('MyApp', 'MyCompany'), STRING_TYPE)
        self.assertIsInstance(
            appdirs.user_state_dir('MyApp', 'MyCompany'), STRING_TYPE)
        self.assertIsInstance(
            appdirs.user_log_dir('MyApp', 'MyCompany'), STRING_TYPE)

    def test_path_helpers(self):
        self.assertIsInstance(
            appdirs.user_data_path('MyApp', 'MyCompany'), PATH_TYPE)
        self.assertIsInstance(
            appdirs.site_data_path('MyApp', 'MyCompany'), PATH_TYPE)
        self.assertIsInstance(
            appdirs.user_cache_path('MyApp', 'MyCompany'), PATH_TYPE)
        self.assertIsInstance(
            appdirs.user_state_path('MyApp', 'MyCompany'), PATH_TYPE)
        self.assertIsInstance(
            appdirs.user_log_path('MyApp', 'MyCompany'), PATH_TYPE)

    def test_dirs(self):
        dirs = appdirs.AppDirs('MyApp', 'MyCompany', version='1.0')
        self.assertIsInstance(dirs.user_data_dir, STRING_TYPE)
        self.assertIsInstance(dirs.site_data_dir, STRING_TYPE)
        self.assertIsInstance(dirs.user_cache_dir, STRING_TYPE)
        self.assertIsInstance(dirs.user_state_dir, STRING_TYPE)
        self.assertIsInstance(dirs.user_log_dir, STRING_TYPE)

    def test_paths(self):
        paths = appdirs.AppPaths('MyApp', 'MyCompany', version='1.0')
        self.assertIsInstance(paths.user_data_dir, PATH_TYPE)
        self.assertIsInstance(paths.site_data_dir, PATH_TYPE)
        self.assertIsInstance(paths.user_cache_dir, PATH_TYPE)
        self.assertIsInstance(paths.user_state_dir, PATH_TYPE)
        self.assertIsInstance(paths.user_log_dir, PATH_TYPE)


if __name__ == "__main__":
    unittest.main()
