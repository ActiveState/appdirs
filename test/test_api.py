import unittest
import appdirs

class Test_AppDir(unittest.TestCase):
    def test_metadata(self):
        self.assertTrue(hasattr(appdirs, "__version__"))
        self.assertTrue(hasattr(appdirs, "__version_info__"))

    def test_helpers(self):
        self.assertTrue(isinstance(
            appdirs.user_data_dir('MyApp', 'MyCompany'), str))
        self.assertTrue(isinstance(
            appdirs.site_data_dir('MyApp', 'MyCompany'), str))
        self.assertTrue(isinstance(
            appdirs.user_cache_dir('MyApp', 'MyCompany'), str))
        self.assertTrue(isinstance(
            appdirs.user_log_dir('MyApp', 'MyCompany'), str))

    def test_dirs(self):
        dirs = appdirs.AppDirs('MyApp', 'MyCompany', version='1.0')
        self.assertTrue(isinstance(dirs.user_data_dir, str))
        self.assertTrue(isinstance(dirs.site_data_dir, str))
        self.assertTrue(isinstance(dirs.user_cache_dir, str))
        self.assertTrue(isinstance(dirs.user_log_dir, str))

if __name__=="__main__":
    unittest.main()
