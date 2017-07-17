#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2005-2010 ActiveState Software Inc.
# Copyright (c) 2013 Eddy Petrișor

"""Utilities for determining application-specific dirs.

See <http://github.com/ActiveState/appdirs> for details and usage.

Notes
-----
  The paths this module returns are based on the following docs:
    - For Windows, it's based on article Q310294[1] and KNOWNFOLDERID[2].
    - For OS X, it's based on Apple's File System Basics docs[3].
    - For *nix, it's based on the XDG Base Directory Specification[4] and
      Debian's state directory proposal[5].

  On Windows and *nix this module is slightly opinionated. The user_log_dir
  function appends 'Logs' on Windows and 'log' on *nix to the path. The
  user_cache_dir function appends 'Cache' on Windows to the path. The rationale
  is explained in the function's docstring.

References
----------
.. [1] https://support.microsoft.com/en-us/kb310294
.. [2] https://msdn.microsoft.com/en-us/library/windows/desktop/dd378457
.. [3] https://developer.apple.com/library/content/documentation/FileManagement/Conceptual/FileSystemProgrammingGuide/FileSystemOverview/FileSystemOverview.html
.. [4] https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html
.. [5] https://wiki.debian.org/XDGBaseDirectorySpecification#state

"""

import sys
import os


__version__ = "1.4.4"
__version_info__ = tuple(int(segment) for segment in __version__.split("."))


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
    r"""The full path to the user-specific data directory.

    This directory should be used to store user-specific data files.

    Parameters
    ----------
    appname : str, optional
        The name of the application, if not specified will return the default
        directory.
    appauthor : str, optional
        The name of the author or distributing body for the application.
        Typically it is the owning company name. This falls back to `appname`
        if None, this can be disabled by passing False.
        `appauthor` is not used on Unix.
    version : str or int or float, optional
        The optional version to append to the path. You might want to use this
        if you want multiple versions of your application to run independently.
        If used, this would typically be '<mayor>.<minor>'.
        Only applied when `appname` is specified.
    roaming : bool, optional
        Use the Windows roaming directory. That means that for users on a
        Windows network setup with roaming profiles, this user's data will by
        sync'd on login. See [TN]_ for a discussion if issues.

    Notes
    -----
    Typical user data directories are:
        Mac OS X:               ~/Library/Application Support/<AppAuthor>/<AppName>
        Unix:                   $XDG_DATA_HOME or ~/.local/share/<AppName>
        Win XP (not roaming):   C:\Documents and Settings\<username>\Application Data\<AppAuthor>\<AppName>
        Win XP (roaming):       C:\Documents and Settings\<username>\Local Settings\Application Data\<AppAuthor>\<AppName>
        Win 7  (not roaming):   C:\Users\<username>\AppData\Local\<AppAuthor>\<AppName>
        Win 7  (roaming):       C:\Users\<username>\AppData\Roaming\<AppAuthor>\<AppName>

    References
    ----------
    .. [TN] https://technet.microsoft.com/en-us/library/cc766489(WS.10).aspx
    """
    if system == "win32":
        if appauthor is None:
            appauthor = appname
        if roaming:
            path = os.getenv('APPDATA', _get_win_folder_from_knownid('{3EB685DB-65F9-4CF6-A03A-E3EF65729F3D}'))
        else:
            path = os.getenv('LOCALAPPDATA', _get_win_folder_from_knownid('{F1B32785-6FBA-4FCF-9D55-7B8E7F157091}'))
    elif system == 'darwin':
        path = os.path.expanduser('~/Library/Application Support/')
    else:
        path = os.getenv('XDG_DATA_HOME', os.path.expanduser("~/.local/share"))
        if appname:
            if version:
                path = os.path.join(path, appname, str(version))
            else:
                path = os.path.join(path, appname)
        return path
    if appname:
        if appauthor:
            path = os.path.join(path, appauthor, appname)
        else:
            path = os.path.join(path, appname)
        if version:
            path = os.path.join(path, str(version))
    return path


def site_data_dir(appname=None, appauthor=None, version=None, multipath=False):
    r"""The full path to the user-shared data directory.

    This directory should be used to store user-shared data files.

    Parameters
    ----------
    appname : str, optional
        The name of the application, if not specified will return the default
        directory.
    appauthor : str, optional
        The name of the author or distributing body for the application.
        Typically it is the owning company name. This falls back to `appname`
        if None, this can be disabled by passing False.
        `appauthor` is not used on Unix.
    version : str or int or float, optional
        The optional version to append to the path. You might want to use this
        if you want multiple versions of your application to run independently.
        If used, this would typically be '<mayor>.<minor>'.
        Only applied when `appname` is specified.
    multipath : bool, optional
        Return the entire list of data directories on *nix. By default only the
        first item in $XDG_DATA_DIRS is returned, or the default path if not set.

    Notes
    -----
    Typical site data directories are:
        Mac OS X:   /Library/Application Support/<AppAuthor>/<AppName>
        Unix:       $XDG_DATA_DIRS[i]/<AppName> or /usr/local/share/<AppName> or
                    /usr/share/<AppName>
        Win XP:     C:\Documents and Settings\All Users\Application Data\<AppAuthor>\<AppName>
        Win 7:      C:\ProgramData\<AppAuthor>\<AppName>

    WARNING: Do not use this on Windows Vista. On Vista the C:\ProgramData is a
    system directory and therefore not writable.
    """
    if system == "win32":
        if appauthor is None:
            appauthor = appname
        path = os.getenv('ALLUSERSPROFILE', _get_win_folder_from_knownid('{62AB5D82-FDC1-4DC3-A9DD-070D1D495D97}'))
    elif system == 'darwin':
        path = os.path.expanduser('/Library/Application Support')
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

    if appname:
        if appauthor:
            path = os.path.join(path, appauthor, appname)
        else:
            path = os.path.join(path, appname)
        if version:
            path = os.path.join(path, str(version))
    return path


def user_config_dir(appname=None, appauthor=None, version=None, roaming=False):
    r"""The full path to the user-specific config directory.

    This directory should be used to store user-specific configuration files.

    Parameters
    ----------
    appname : str, optional
        The name of the application, if not specified will return the default
        directory.
    appauthor : str, optional
        The name of the author or distributing body for the application.
        Typically it is the owning company name. This falls back to `appname`
        if None, this can be disabled by passing False.
        `appauthor` is not used on Unix.
    version : str or int or float, optional
        The optional version to append to the path. You might want to use this
        if you want multiple versions of your application to run independently.
        If used, this would typically be '<mayor>.<minor>'.
        Only applied when `appname` is specified.
    roaming : bool, optional
        Use the Windows roaming directory. That means that for users on a
        Windows network setup with roaming profiles, this user's data will by
        sync'd on login. See [TN]_ for a discussion if issues.

    Notes
    -----
    Typical user config directories are:
        Mac OS X:               same as user_data_dir
        Unix:                   $XDG_CONFIG_HOME or ~/.config/<AppName>
        Win *:                  same as user_data_dir

    References
    ----------
    .. [TN] https://technet.microsoft.com/en-us/library/cc766489(WS.10).aspx
    """
    if system in ["win32", "darwin"]:
        return user_data_dir(appname, appauthor, version, roaming)
    else:
        path = os.getenv('XDG_CONFIG_HOME', os.path.expanduser("~/.config"))
        if appname:
            if version:
                path = os.path.join(path, appname, str(version))
            else:
                path = os.path.join(path, appname)
    return path


def site_config_dir(appname=None, appauthor=None, version=None, multipath=False):
    r"""The full path to the user-shared data directory.

    This directory should be used to store user-shared configuration files.

    Parameters
    ----------
    appname : str, optional
        The name of the application, if not specified will return the default
        directory.
    appauthor : str, optional
        The name of the author or distributing body for the application.
        Typically it is the owning company name. This falls back to `appname`
        if None, this can be disabled by passing False.
        `appauthor` is not used on Unix.
    version : str or int or float, optional
        The optional version to append to the path. You might want to use this
        if you want multiple versions of your application to run independently.
        If used, this would typically be '<mayor>.<minor>'.
        Only applied when `appname` is specified.
    multipath : bool, optional
        Return the entire list of config directories on *nix. By default only
        the first item in $XDG_CONFIG_DIRS is returned, or the default path if
        not set.

    Notes
    -----
    Typical site config directories are:
        Mac OS X:   same as site_data_dir
        Unix:       $XDG_CONFIG_DIRS[i]/<AppName> or /etc/xdg/<AppName>
        Win *:      same as site_data_dir

    WARNING: Do not use this on Windows Vista. On Vista the C:\ProgramData is a
    system directory and therefore not writable.
    """
    if system in ["win32", "darwin"]:
        return site_data_dir(appname, appauthor, version)
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
    r"""The full path to the user-specific cache directory.

    This directory should be used to store user-specific non-essential (cached)
    data files. This directory might be in a TMPFS and may not survive a reboot.

    Parameters
    ----------
    appname : str, optional
        The name of the application, if not specified will return the default
        directory.
    appauthor : str, optional
        The name of the author or distributing body for the application.
        Typically it is the owning company name. This falls back to `appname`
        if None, this can be disabled by passing False.
        `appauthor` is not used on Unix.
    version : str or int or float, optional
        The optional version to append to the path. You might want to use this
        if you want multiple versions of your application to run independently.
        If used, this would typically be '<mayor>.<minor>'.
        Only applied when `appname` is specified.
    opinion : bool, optional
        Disable the appending of 'Cache' to the returned path on Windows.
        See the Notes section below for the rationale

    Notes
    -----
    Typical user cache directories are:
        Mac OS X:   ~/Library/Caches/AppAuthor>/<AppName>
        Unix:       $XDG_CACHE_HOME or ~/.cache/<AppName>
        Win XP:     C:\Documents and Settings\<username>\Local Settings\Application Data\<AppAuthor>\<AppName>\Cache
        Vista:      C:\Users\<username>\AppData\Local\<AppAuthor>\<AppName>\Cache

    On Windows the only suggestion in the MSDN docs is that local settings go in
    the `CSIDL_LOCAL_APPDATA` directory. This is identical to the non-roaming
    app data dir (the default returned by `user_data_dir` above). Apps typically
    put cache data somewhere *under* the given dir here. Some examples:
        ...\Mozilla\Firefox\Profiles\<ProfileName>\Cache
        ...\Acme\SuperApp\Cache\1.0
    Opinion: This function appends "Cache" to the `CSIDL_LOCAL_APPDATA` value.
    This can be disabled with the `opinion=False` option.
    """
    if system == "win32":
        if appauthor is None:
            appauthor = appname
        path = os.getenv('LOCALAPPDATA', _get_win_folder_from_knownid('{F1B32785-6FBA-4FCF-9D55-7B8E7F157091}'))
        if appname:
            if appauthor:
                path = os.path.join(path, appauthor, appname)
            else:
                path = os.path.join(path, appname)
            if opinion:
                path = os.path.join(path, "Cache")
    elif system == 'darwin':
        path = os.path.expanduser('~/Library/Caches')
        if appname:
            if appauthor:
                path = os.path.join(path, appauthor, appname)
            else:
                path = os.path.join(path, appname)
    else:
        path = os.getenv('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
        if appname:
            path = os.path.join(path, appname)
    if appname and version:
        path = os.path.join(path, str(version))
    return path


def user_state_dir(appname=None, appauthor=None, version=None, roaming=False):
    r"""The full path to the user-specific state dir for this application.

    This directory should be used to store user-specific non-essential files
    which should survive a reboot. For example: recently opened files or last
    time application was run.

    Parameters
    ----------
    appname : str, optional
        The name of the application, if not specified will return the default
        directory.
    appauthor : str, optional
        The name of the author or distributing body for the application.
        Typically it is the owning company name. This falls back to `appname`
        if None, this can be disabled by passing False.
        `appauthor` is not used on Unix.
    version : str or int or float, optional
        The optional version to append to the path. You might want to use this
        if you want multiple versions of your application to run independently.
        If used, this would typically be '<mayor>.<minor>'.
        Only applied when `appname` is specified.
    roaming : bool, optional
        Use the Windows roaming directory. That means that for users on a
        Windows network setup with roaming profiles, this user's data will by
        sync'd on login. See [TN]_ for a discussion if issues.

    Notes
    -----
    Typical user state directories are:
        Mac OS X:  same as user_data_dir
        Unix:      $XDG_STATE_HOME or ~/.local/state/<AppName>
        Win *:     same as user_data_dir

    References
    ----------
    .. [TN] https://technet.microsoft.com/en-us/library/cc766489(WS.10).aspx
    """
    if system in ["win32", "darwin"]:
        return user_data_dir(appname, appauthor, version, roaming)
    else:
        path = os.getenv('XDG_STATE_HOME', os.path.expanduser("~/.local/state"))
        if appname:
            if version:
                path = os.path.join(path, appname, str(version))
            else:
                path = os.path.join(path, appname)
    return path


def user_log_dir(appname=None, appauthor=None, version=None, opinion=True):
    r"""The full path to the user-specific log directory.

    This directory should be used to store user-specific log files.

    Parameters
    ----------
    appname : str, optional
        The name of the application, if not specified will return the default
        directory.
    appauthor : str, optional
        The name of the author or distributing body for the application.
        Typically it is the owning company name. This falls back to `appname`
        if None, this can be disabled by passing False.
        `appauthor` is not used on Unix.
    version : str or int or float, optional
        The optional version to append to the path. You might want to use this
        if you want multiple versions of your application to run independently.
        If used, this would typically be '<mayor>.<minor>'.
        Only applied when `appname` is specified.
    opinion : bool, optional
        Disable the appending of 'Logs' on Windows and 'log' on *nix to the
        returned path. See the Notes section below for the rationale

    Notes
    -----
    Typical user log directories are:
        Mac OS X:   ~/Library/Logs/AppAuthor>/<AppName>
        Unix:       $XDG_CACHE_HOME/<AppName>/log or ~/.cache/<AppName>/log
        Win XP:     C:\Documents and Settings\<username>\Local Settings\Application Data\<AppAuthor>\<AppName>\Logs
        Vista:      C:\Users\<username>\AppData\Local\<AppAuthor>\<AppName>\Logs

    On Windows the only suggestion in the MSDN docs is that local settings
    go in the `CSIDL_LOCAL_APPDATA` directory. (Note: Any examples on Windows
    and *nix of log directories are welcome.)

    Opinion: This function appends "Logs" to the `CSIDL_LOCAL_APPDATA`
    value for Windows and appends "log" to the user cache dir for Unix.
    This can be disabled with the `opinion=False` option.
    """
    if system == "darwin":
        path = os.path.expanduser('~/Library/Logs')
        if appname:
            if appauthor:
                path = os.path.join(path, appauthor, appname)
            else:
                path = os.path.join(path, appname)
            if version:
                path = os.path.join(path, str(version))
    elif system == "win32":
        path = user_data_dir(appname, appauthor, version)
        if opinion:
            path = os.path.join(path, "Logs")
    else:
        path = user_cache_dir(appname, appauthor, version)
        if opinion:
            path = os.path.join(path, "log")
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
        """The full path to the user specific data directory."""
        return user_data_dir(self.appname, self.appauthor,
                             version=self.version, roaming=self.roaming)

    @property
    def site_data_dir(self):
        """The full path to the user-shared data directory."""
        return site_data_dir(self.appname, self.appauthor,
                             version=self.version, multipath=self.multipath)

    @property
    def user_config_dir(self):
        """The full path to the user-specific config directory."""
        return user_config_dir(self.appname, self.appauthor,
                               version=self.version, roaming=self.roaming)

    @property
    def site_config_dir(self):
        """The full path to the user-shared data directory."""
        return site_config_dir(self.appname, self.appauthor,
                               version=self.version, multipath=self.multipath)

    @property
    def user_cache_dir(self):
        """The full path to the user-specific cache directory."""
        return user_cache_dir(self.appname, self.appauthor,
                              version=self.version)

    @property
    def user_state_dir(self):
        """The full path to the user-specific state directory."""
        return user_state_dir(self.appname, self.appauthor,
                              version=self.version)

    @property
    def user_log_dir(self):
        """The full path to the user-specific log directory."""
        return user_log_dir(self.appname, self.appauthor,
                            version=self.version)


# internal support stuff

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
