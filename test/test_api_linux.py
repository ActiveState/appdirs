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

env = ['XDG_DATA_HOME',
       'XDG_DATA_DIRS',
       'XDG_CONFIG_HOME',
       'XDG_CONFIG_DIRS',
       'XDG_CACHE_HOME',
       'XDG_STATE_HOME',
       'XDG_DESKTOP_DIR',
       'XDG_DOCUMENTS_DIR',
       'XDG_DOWNLOAD_DIR',
       'XDG_MUSIC_DIR',
       'XDG_PICTURES_DIR',
       'XDG_PUBLICSHARE_DIR',
       'XDG_TEMPLATES_DIR',
       'XDG_VIDEOS_DIR']


class TestLinuxWithXDG(unittest.TestCase):
    def setUp(self):
        appdirs.system = 'linux'
        os.environ['USER'] = "travis"
        os.environ['HOME'] = "/home/travis"
        os.environ['XDG_DATA_HOME'] = "/test/xdg/data/home"
        os.environ['XDG_DATA_DIRS'] = "/test/xdg/data/dirs:/xdg/test/data/dirs"
        os.environ['XDG_CONFIG_HOME'] = "/test/xdg/config/home"
        os.environ['XDG_CONFIG_DIRS'] = "/test/xdg/config/dirs:/xdg/test/config/dirs"
        os.environ['XDG_CACHE_HOME'] = "/test/xdg/cache/home"
        os.environ['XDG_STATE_HOME'] = "/test/xdg/state/home"

    def test_wrapper(self):
        dirs = appdirs.AppDirs('MyApp', 'MyCompany', version=1.0, multipath=True)
        self.assertEqual(dirs.user_data_dir, "/test/xdg/data/home/MyApp/1.0")
        self.assertEqual(dirs.site_data_dir, "/test/xdg/data/dirs/MyApp/1.0:/xdg/test/data/dirs/MyApp/1.0")
        self.assertEqual(dirs.user_config_dir, "/test/xdg/config/home/MyApp/1.0")
        self.assertEqual(dirs.site_config_dir, "/test/xdg/config/dirs/MyApp/1.0:/xdg/test/config/dirs/MyApp/1.0")
        self.assertEqual(dirs.user_cache_dir, "/test/xdg/cache/home/MyApp/1.0")
        self.assertEqual(dirs.user_state_dir, "/test/xdg/state/home/MyApp/1.0")
        self.assertEqual(dirs.user_log_dir, "/test/xdg/cache/home/MyApp/1.0/log")

    def test_program_dirs(self):
        self.assertEqual(
            appdirs.user_data_dir('MyApp', 'MyCompany', 1.0), "/test/xdg/data/home/MyApp/1.0")
        self.assertEqual(
            appdirs.site_data_dir('MyApp', 'MyCompany', 1.0, multipath=True), "/test/xdg/data/dirs/MyApp/1.0:/xdg/test/data/dirs/MyApp/1.0")
        self.assertEqual(
            appdirs.user_config_dir('MyApp', 'MyCompany', 1.0), "/test/xdg/config/home/MyApp/1.0")
        self.assertEqual(
            appdirs.site_config_dir('MyApp', 'MyCompany', 1.0, multipath=True), "/test/xdg/config/dirs/MyApp/1.0:/xdg/test/config/dirs/MyApp/1.0")
        self.assertEqual(
            appdirs.user_cache_dir('MyApp', 'MyCompany', 1.0), "/test/xdg/cache/home/MyApp/1.0")
        self.assertEqual(
            appdirs.user_state_dir('MyApp', 'MyCompany', 1.0), "/test/xdg/state/home/MyApp/1.0")
        self.assertEqual(
            appdirs.user_log_dir('MyApp', 'MyCompany', 1.0), "/test/xdg/cache/home/MyApp/1.0/log")

    def tearDown(self):
        for i in env:
            try:
                del os.environ[i]
            except KeyError:
                continue


class TestLinuxWithoutXDG(unittest.TestCase):
    def setUp(self):
        appdirs.system = 'linux'
        os.environ['USER'] = "travis"
        os.environ['HOME'] = "/home/travis"
        for i in env:
            try:
                del os.environ[i]
            except KeyError:
                continue

    def test_wrapper(self):
        dirs = appdirs.AppDirs('MyApp', 'MyCompany', version=1.0)
        self.assertEqual(dirs.user_data_dir, "/home/travis/.local/share/MyApp/1.0")
        self.assertEqual(dirs.site_data_dir, "/usr/local/share/MyApp/1.0")
        self.assertEqual(dirs.user_config_dir, "/home/travis/.config/MyApp/1.0")
        self.assertEqual(dirs.site_config_dir, "/etc/xdg/MyApp/1.0")
        self.assertEqual(dirs.user_cache_dir, "/home/travis/.cache/MyApp/1.0")
        self.assertEqual(dirs.user_state_dir, "/home/travis/.local/state/MyApp/1.0")
        self.assertEqual(dirs.user_log_dir, "/home/travis/.cache/MyApp/1.0/log")

    def test_program_dirs(self):
        self.assertEqual(
            appdirs.user_data_dir('MyApp', 'MyCompany', 1.0), "/home/travis/.local/share/MyApp/1.0")
        self.assertEqual(
            appdirs.site_data_dir('MyApp', 'MyCompany', 1.0), "/usr/local/share/MyApp/1.0")
        self.assertEqual(
            appdirs.user_config_dir('MyApp', 'MyCompany', 1.0), "/home/travis/.config/MyApp/1.0")
        self.assertEqual(
            appdirs.site_config_dir('MyApp', 'MyCompany', 1.0), "/etc/xdg/MyApp/1.0")
        self.assertEqual(
            appdirs.user_cache_dir('MyApp', 'MyCompany', 1.0), "/home/travis/.cache/MyApp/1.0")
        self.assertEqual(
            appdirs.user_state_dir('MyApp', 'MyCompany', 1.0), "/home/travis/.local/state/MyApp/1.0")
        self.assertEqual(
            appdirs.user_log_dir('MyApp', 'MyCompany', 1.0), "/home/travis/.cache/MyApp/1.0/log")


class TestAppDir(unittest.TestCase):
    def test_metadata(self):
        self.assertTrue(hasattr(appdirs, "__version__"))
        self.assertTrue(hasattr(appdirs, "__version_info__"))

if __name__ == "__main__":
    print("Starting tests")
    unittest.main()
