#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2005-2010 ActiveState Software Inc.
# Copyright (c) 2013 Eddy Petrișor

"""Utilities for determining application-specific dirs.

See <http://github.com/ActiveState/appdirs> for details and usage.
"""
# Dev Notes:
# - MSDN on where to store app data files:
#   http://support.microsoft.com/default.aspx?scid=kb;en-us;310294#XSLTH3194121123120121120120
#   https://msdn.microsoft.com/en-us/library/windows/desktop/dd378457(v=vs.85).aspx
# - Mac OS X:
#   https://developer.apple.com/library/content/documentation/FileManagement/Conceptual/FileSystemProgrammingGuide/FileSystemOverview/FileSystemOverview.html
# - XDG spec for Un*x: http://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html

__version__ = "1.4.4"
__version_info__ = tuple(int(segment) for segment in __version__.split("."))


import sys
import os

PY3 = sys.version_info[0] == 3

if PY3:
    unicode = str

if sys.platform.startswith('java'):
    import platform
    os_name = platform.java_ver()[3][0]
    if os_name.startswith('Windows'): # "Windows XP", "Windows 7", etc.
        system = 'win32'
    elif os_name.startswith('Mac'): # "Mac OS X", etc.
        system = 'darwin'
    else: # "Linux", "SunOS", "FreeBSD", etc.
        # Setting this to "linux2" is not ideal, but only Windows or Mac
        # are actually checked for and the rest of the module expects
        # *sys.platform* style strings.
        system = 'linux2'
else:
    system = sys.platform



def user_data_dir(appname=None, appauthor=None, version=None, roaming=False):
    r"""Return full path to the user-specific data dir for this application.

        "appname" is the name of application.
            If None, just the system directory is returned.
        "appauthor" (only used on Windows) is the name of the
            appauthor or distributing body for this application. Typically
            it is the owning company name. This falls back to appname. You may
            pass False to disable it.
        "version" is an optional version path element to append to the
            path. You might want to use this if you want multiple versions
            of your app to be able to run independently. If used, this
            would typically be "<major>.<minor>".
            Only applied when appname is present.
        "roaming" (boolean, default False) can be set True to use the Windows
            roaming appdata directory. That means that for users on a Windows
            network setup for roaming profiles, this user data will be
            sync'd on login. See
            <http://technet.microsoft.com/en-us/library/cc766489(WS.10).aspx>
            for a discussion of issues.

    Typical user data directories are:
        Mac OS X:               ~/Library/Application Support/<AppName>
        Unix:                   ~/.local/share/<AppName>    # or in $XDG_DATA_HOME, if defined
        Win XP (not roaming):   C:\Documents and Settings\<username>\Application Data\<AppAuthor>\<AppName>
        Win XP (roaming):       C:\Documents and Settings\<username>\Local Settings\Application Data\<AppAuthor>\<AppName>
        Win 7  (not roaming):   C:\Users\<username>\AppData\Local\<AppAuthor>\<AppName>
        Win 7  (roaming):       C:\Users\<username>\AppData\Roaming\<AppAuthor>\<AppName>

    For Unix, we follow the XDG spec and support $XDG_DATA_HOME.
    That means, by default "~/.local/share/<AppName>".
    """
    if system == "win32":
        if appauthor is None:
            appauthor = appname
        if roaming:
            path = os.getenv('APPDATA', _get_win_folder_from_knownid('{3EB685DB-65F9-4CF6-A03A-E3EF65729F3D}'))
        else:
            path = os.getenv('LOCALAPPDATA', _get_win_folder_from_knownid('{F1B32785-6FBA-4FCF-9D55-7B8E7F157091}'))
        if appname:
            if appauthor:
                path = os.path.join(path, appauthor, appname)
            else:
                path = os.path.join(path, appname)
    elif system == 'darwin':
        path = os.path.expanduser('~/Library/Application Support/')
        if appname:
            path = os.path.join(path, appname)
    else:
        path = os.getenv('XDG_DATA_HOME', os.path.expanduser("~/.local/share"))
        if appname:
            path = os.path.join(path, appname)
    if appname and version:
        path = os.path.join(path, str(version))
    return path


def site_data_dir(appname=None, appauthor=None, version=None, multipath=False):
    r"""Return full path to the user-shared data dir for this application.

        "appname" is the name of application.
            If None, just the system directory is returned.
        "appauthor" (only used on Windows) is the name of the
            appauthor or distributing body for this application. Typically
            it is the owning company name. This falls back to appname. You may
            pass False to disable it.
        "version" is an optional version path element to append to the
            path. You might want to use this if you want multiple versions
            of your app to be able to run independently. If used, this
            would typically be "<major>.<minor>".
            Only applied when appname is present.
        "multipath" is an optional parameter only applicable to *nix
            which indicates that the entire list of data dirs should be
            returned. By default, the first item from XDG_DATA_DIRS is
            returned, or '/usr/local/share/<AppName>',
            if XDG_DATA_DIRS is not set

    Typical site data directories are:
        Mac OS X:   /Library/Application Support/<AppName>
        Unix:       /usr/local/share/<AppName> or /usr/share/<AppName>
        Win XP:     C:\Documents and Settings\All Users\Application Data\<AppAuthor>\<AppName>
        Vista:      (Fail! "C:\ProgramData" is a hidden *system* directory on Vista.)
        Win 7:      C:\ProgramData\<AppAuthor>\<AppName>   # Hidden, but writeable on Win 7.

    For Unix, this is using the $XDG_DATA_DIRS[0] default.

    WARNING: Do not use this on Windows. See the Vista-Fail note above for why.
    """
    if system == "win32":
        if appauthor is None:
            appauthor = appname
        path = os.getenv('ALLUSERSPROFILE', _get_win_folder_from_knownid('{62AB5D82-FDC1-4DC3-A9DD-070D1D495D97}'))
        if appname:
            if appauthor is not False:
                path = os.path.join(path, appauthor, appname)
            else:
                path = os.path.join(path, appname)
    elif system == 'darwin':
        path = os.path.expanduser('/Library/Application Support')
        if appname:
            path = os.path.join(path, appname)
    else:
        # XDG default for $XDG_DATA_DIRS
        # only first, if multipath is False
        path = os.getenv('XDG_DATA_DIRS',
                         os.pathsep.join(['/usr/local/share', '/usr/share']))
        pathlist = [os.path.expanduser(x.rstrip(os.sep)) for x in path.split(os.pathsep)]
        if appname:
            if version:
                appname = os.path.join(appname, str(version))
            pathlist = [os.sep.join([x, appname]) for x in pathlist]

        if multipath:
            path = os.pathsep.join(pathlist)
        else:
            path = pathlist[0]
        return path

    if appname and version:
        path = os.path.join(path, str(version))
    return path


def user_config_dir(appname=None, appauthor=None, version=None, roaming=False):
    r"""Return full path to the user-specific config dir for this application.

        "appname" is the name of application.
            If None, just the system directory is returned.
        "appauthor" (only used on Windows) is the name of the
            appauthor or distributing body for this application. Typically
            it is the owning company name. This falls back to appname. You may
            pass False to disable it.
        "version" is an optional version path element to append to the
            path. You might want to use this if you want multiple versions
            of your app to be able to run independently. If used, this
            would typically be "<major>.<minor>".
            Only applied when appname is present.
        "roaming" (boolean, default False) can be set True to use the Windows
            roaming appdata directory. That means that for users on a Windows
            network setup for roaming profiles, this user data will be
            sync'd on login. See
            <http://technet.microsoft.com/en-us/library/cc766489(WS.10).aspx>
            for a discussion of issues.

    Typical user config directories are:
        Mac OS X:               same as user_data_dir
        Unix:                   ~/.config/<AppName>     # or in $XDG_CONFIG_HOME, if defined
        Win *:                  same as user_data_dir

    For Unix, we follow the XDG spec and support $XDG_CONFIG_HOME.
    That means, by default "~/.config/<AppName>".
    """
    if system in ["win32", "darwin"]:
        path = user_data_dir(appname, appauthor, None, roaming)
    else:
        path = os.getenv('XDG_CONFIG_HOME', os.path.expanduser("~/.config"))
        if appname:
            path = os.path.join(path, appname)
    if appname and version:
        path = os.path.join(path, str(version))
    return path


def site_config_dir(appname=None, appauthor=None, version=None, multipath=False):
    r"""Return full path to the user-shared data dir for this application.

        "appname" is the name of application.
            If None, just the system directory is returned.
        "appauthor" (only used on Windows) is the name of the
            appauthor or distributing body for this application. Typically
            it is the owning company name. This falls back to appname. You may
            pass False to disable it.
        "version" is an optional version path element to append to the
            path. You might want to use this if you want multiple versions
            of your app to be able to run independently. If used, this
            would typically be "<major>.<minor>".
            Only applied when appname is present.
        "multipath" is an optional parameter only applicable to *nix
            which indicates that the entire list of config dirs should be
            returned. By default, the first item from XDG_CONFIG_DIRS is
            returned, or '/etc/xdg/<AppName>', if XDG_CONFIG_DIRS is not set

    Typical site config directories are:
        Mac OS X:   same as site_data_dir
        Unix:       /etc/xdg/<AppName> or $XDG_CONFIG_DIRS[i]/<AppName> for each value in
                    $XDG_CONFIG_DIRS
        Win *:      same as site_data_dir
        Vista:      (Fail! "C:\ProgramData" is a hidden *system* directory on Vista.)

    For Unix, this is using the $XDG_CONFIG_DIRS[0] default, if multipath=False

    WARNING: Do not use this on Windows. See the Vista-Fail note above for why.
    """
    if system in ["win32", "darwin"]:
        path = site_data_dir(appname, appauthor)
        if appname and version:
            path = os.path.join(path, str(version))
    else:
        # XDG default for $XDG_CONFIG_DIRS
        # only first, if multipath is False
        path = os.getenv('XDG_CONFIG_DIRS', '/etc/xdg')
        pathlist = [os.path.expanduser(x.rstrip(os.sep)) for x in path.split(os.pathsep)]
        if appname:
            if version:
                appname = os.path.join(appname, str(version))
            pathlist = [os.sep.join([x, appname]) for x in pathlist]

        if multipath:
            path = os.pathsep.join(pathlist)
        else:
            path = pathlist[0]
    return path


def user_cache_dir(appname=None, appauthor=None, version=None, opinion=True):
    r"""Return full path to the user-specific cache dir for this application.

        "appname" is the name of application.
            If None, just the system directory is returned.
        "appauthor" (only used on Windows) is the name of the
            appauthor or distributing body for this application. Typically
            it is the owning company name. This falls back to appname. You may
            pass False to disable it.
        "version" is an optional version path element to append to the
            path. You might want to use this if you want multiple versions
            of your app to be able to run independently. If used, this
            would typically be "<major>.<minor>".
            Only applied when appname is present.
        "opinion" (boolean) can be False to disable the appending of
            "Cache" to the base app data dir for Windows. See
            discussion below.

    Typical user cache directories are:
        Mac OS X:   ~/Library/Caches/<AppName>
        Unix:       ~/.cache/<AppName> (XDG default)
        Win XP:     C:\Documents and Settings\<username>\Local Settings\Application Data\<AppAuthor>\<AppName>\Cache
        Vista:      C:\Users\<username>\AppData\Local\<AppAuthor>\<AppName>\Cache

    On Windows the only suggestion in the MSDN docs is that local settings go in
    the `CSIDL_LOCAL_APPDATA` directory. This is identical to the non-roaming
    app data dir (the default returned by `user_data_dir` above). Apps typically
    put cache data somewhere *under* the given dir here. Some examples:
        ...\Mozilla\Firefox\Profiles\<ProfileName>\Cache
        ...\Acme\SuperApp\Cache\1.0
    OPINION: This function appends "Cache" to the `CSIDL_LOCAL_APPDATA` value.
    This can be disabled with the `opinion=False` option.
    """
    if system == "win32":
        if appauthor is None:
            appauthor = appname
        path = os.getenv('LOCALAPPDATA', _get_win_folder_from_knownid('{F1B32785-6FBA-4FCF-9D55-7B8E7F157091}'))
        if appname:
            if appauthor is not False:
                path = os.path.join(path, appauthor, appname)
            else:
                path = os.path.join(path, appname)
            if opinion:
                path = os.path.join(path, "Cache")
    elif system == 'darwin':
        path = os.path.expanduser('~/Library/Caches')
        if appname:
            path = os.path.join(path, appname)
    else:
        path = os.getenv('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
        if appname:
            path = os.path.join(path, appname)
    if appname and version:
        path = os.path.join(path, str(version))
    return path


def user_state_dir(appname=None, appauthor=None, version=None, roaming=False):
    r"""Return full path to the user-specific state dir for this application.

        "appname" is the name of application.
            If None, just the system directory is returned.
        "appauthor" (only used on Windows) is the name of the
            appauthor or distributing body for this application. Typically
            it is the owning company name. This falls back to appname. You may
            pass False to disable it.
        "version" is an optional version path element to append to the
            path. You might want to use this if you want multiple versions
            of your app to be able to run independently. If used, this
            would typically be "<major>.<minor>".
            Only applied when appname is present.
        "roaming" (boolean, default False) can be set True to use the Windows
            roaming appdata directory. That means that for users on a Windows
            network setup for roaming profiles, this user data will be
            sync'd on login. See
            <http://technet.microsoft.com/en-us/library/cc766489(WS.10).aspx>
            for a discussion of issues.

    Typical user state directories are:
        Mac OS X:  same as user_data_dir
        Unix:      ~/.local/state/<AppName>   # or in $XDG_STATE_HOME, if defined
        Win *:     same as user_data_dir

    For Unix, we follow this Debian proposal <https://wiki.debian.org/XDGBaseDirectorySpecification#state>
    to extend the XDG spec and support $XDG_STATE_HOME.

    That means, by default "~/.local/state/<AppName>".
    """
    if system in ["win32", "darwin"]:
        path = user_data_dir(appname, appauthor, None, roaming)
    else:
        path = os.getenv('XDG_STATE_HOME', os.path.expanduser("~/.local/state"))
        if appname:
            path = os.path.join(path, appname)
    if appname and version:
        path = os.path.join(path, str(version))
    return path


def user_log_dir(appname=None, appauthor=None, version=None, opinion=True):
    r"""Return full path to the user-specific log dir for this application.

        "appname" is the name of application.
            If None, just the system directory is returned.
        "appauthor" (only used on Windows) is the name of the
            appauthor or distributing body for this application. Typically
            it is the owning company name. This falls back to appname. You may
            pass False to disable it.
        "version" is an optional version path element to append to the
            path. You might want to use this if you want multiple versions
            of your app to be able to run independently. If used, this
            would typically be "<major>.<minor>".
            Only applied when appname is present.
        "opinion" (boolean) can be False to disable the appending of
            "Logs" to the base app data dir for Windows, and "log" to the
            base cache dir for Unix. See discussion below.

    Typical user log directories are:
        Mac OS X:   ~/Library/Logs/<AppName>
        Unix:       ~/.cache/<AppName>/log  # or under $XDG_CACHE_HOME if defined
        Win XP:     C:\Documents and Settings\<username>\Local Settings\Application Data\<AppAuthor>\<AppName>\Logs
        Vista:      C:\Users\<username>\AppData\Local\<AppAuthor>\<AppName>\Logs

    On Windows the only suggestion in the MSDN docs is that local settings
    go in the `CSIDL_LOCAL_APPDATA` directory. (Note: I'm interested in
    examples of what some windows apps use for a logs dir.)

    OPINION: This function appends "Logs" to the `CSIDL_LOCAL_APPDATA`
    value for Windows and appends "log" to the user cache dir for Unix.
    This can be disabled with the `opinion=False` option.
    """
    if system == "darwin":
        path = os.path.join(
            os.path.expanduser('~/Library/Logs'),
            appname)
    elif system == "win32":
        path = user_data_dir(appname, appauthor, str(version))
        version = False
        if opinion:
            path = os.path.join(path, "Logs")
    else:
        path = user_cache_dir(appname, appauthor, str(version))
        version = False
        if opinion:
            path = os.path.join(path, "log")
    if appname and version:
        path = os.path.join(path, str(version))
    return path


class AppDirs(object):
    """Convenience wrapper for getting application dirs."""
    def __init__(self, appname=None, appauthor=None, version=None,
            roaming=False, multipath=False):
        self.appname = appname
        self.appauthor = appauthor
        self.version = version
        self.roaming = roaming
        self.multipath = multipath

    @property
    def user_data_dir(self):
        return user_data_dir(self.appname, self.appauthor,
                             version=self.version, roaming=self.roaming)

    @property
    def site_data_dir(self):
        return site_data_dir(self.appname, self.appauthor,
                             version=self.version, multipath=self.multipath)

    @property
    def user_config_dir(self):
        return user_config_dir(self.appname, self.appauthor,
                               version=self.version, roaming=self.roaming)

    @property
    def site_config_dir(self):
        return site_config_dir(self.appname, self.appauthor,
                               version=self.version, multipath=self.multipath)

    @property
    def user_cache_dir(self):
        return user_cache_dir(self.appname, self.appauthor,
                              version=self.version)

    @property
    def user_state_dir(self):
        return user_state_dir(self.appname, self.appauthor,
                              version=self.version)

    @property
    def user_log_dir(self):
        return user_log_dir(self.appname, self.appauthor,
                            version=self.version)


#---- internal support stuff

def _get_win_folder_from_knownid(folderid, userhandle=0):
    """Get folder path from KNOWNFOLDERID.

    Based of code by mkropat [https://gist.github.com/mkropat/7550097] licensed under MIT.

    Params
    ------
    folderid:
        A GUID listed at [https://msdn.microsoft.com/en-us/library/windows/desktop/dd378457.aspx]
    userhandle:
        0 for current user, -1 for common/shared folder
    """
    import ctypes
    from ctypes import windll, wintypes
    from uuid import UUID


    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", wintypes.BYTE * 8)
        ]

        def __init__(self, uuid_):
            ctypes.Structure.__init__(self)
            self.Data1, self.Data2, self.Data3, self.Data4[0], self.Data4[1], rest = uuid_.fields
            for i in range(2, 8):
                self.Data4[i] = rest>>(8 - i - 1)*8 & 0xff

    _CoTaskMemFree = windll.ole32.CoTaskMemFree
    _CoTaskMemFree.restype = None
    _CoTaskMemFree.argtypes = [ctypes.c_void_p]

    _SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
    _SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(GUID), wintypes.DWORD, wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
    ]

    fid = GUID(UUID(folderid))
    pPath = ctypes.c_wchar_p()
    if _SHGetKnownFolderPath(ctypes.byref(fid), 0, userhandle, ctypes.byref(pPath)) != 0:
        raise WindowsError("Path not found for folderid: %s and userhandle: %s" % (folderid, userhandle))
    path = pPath.value
    _CoTaskMemFree(pPath)
    return path


#---- self test code

if __name__ == "__main__":
    appname = "MyApp"
    appauthor = "MyCompany"

    props = ("user_data_dir",
             "user_config_dir",
             "user_cache_dir",
             "user_state_dir",
             "user_log_dir",
             "site_data_dir",
             "site_config_dir")

    print("-- app dirs %s --" % __version__)

    print("-- app dirs (with optional 'version')")
    dirs = AppDirs(appname, appauthor, version="1.0")
    for prop in props:
        print("%s: %s" % (prop, getattr(dirs, prop)))

    print("\n-- app dirs (without optional 'version')")
    dirs = AppDirs(appname, appauthor)
    for prop in props:
        print("%s: %s" % (prop, getattr(dirs, prop)))

    print("\n-- app dirs (without optional 'appauthor')")
    dirs = AppDirs(appname)
    for prop in props:
        print("%s: %s" % (prop, getattr(dirs, prop)))

    print("\n-- app dirs (with disabled 'appauthor')")
    dirs = AppDirs(appname, appauthor=False)
    for prop in props:
        print("%s: %s" % (prop, getattr(dirs, prop)))
