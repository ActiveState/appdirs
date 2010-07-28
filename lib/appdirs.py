#!/usr/bin/env python
# Copyright (c) 2005-2010 ActiveState Software Inc.

"""Utilities for determining application-specific dirs.

See <http://github.com/ActiveState/appdirs> for details and usage.
"""
# Dev Notes:
# - MSDN on where to store app data files:
#   http://support.microsoft.com/default.aspx?scid=kb;en-us;310294#XSLTH3194121123120121120120
# - Mac OS X: http://developer.apple.com/documentation/MacOSX/Conceptual/BPFileSystem/index.html

__version_info__ = (1, 0, 1)
__version__ = '.'.join(map(str, __version_info__))


import sys
import os


class AppDirsError(Exception):
    pass



def user_data_dir(appname, appauthor=None, version=None, roaming=False):
    r"""Return full path to the user-specific data dir for this application.
    
        "appname" is the name of application.
        "appauthor" (only required and used on Windows) is the name of the
            appauthor or distributing body for this application. Typically
            it is the owning company name.
        "version" is an optional version path element to append to the
            path. You might want to use this if you want multiple versions
            of your app to be able to run independently. If used, this
            would typically be "<major>.<minor>".
        "roaming" (boolean, default False) can be set True to use the Windows
            roaming appdata directory. That means that for users on a Windows
            network setup for roaming profiles, this user data will be
            sync'd on login. See
            <http://technet.microsoft.com/en-us/library/cc766489(WS.10).aspx>
            for a discussion of issues.
    
    Typical user data directories are:
        Mac OS X:               ~/Library/Application Support/<AppName>
        Unix:                   ~/.<appname>
        Win XP (not roaming):   C:\Documents and Settings\<username>\Application Data\<AppAuthor>\<AppName>
        Win XP (roaming):       C:\Documents and Settings\<username>\Local Settings\Application Data\<AppAuthor>\<AppName>
        Vista  (not roaming):   C:\Users\<username>\AppData\Local\<AppAuthor>\<AppName>
        Vista  (roaming):       C:\Users\<username>\AppData\Roaming\<AppAuthor>\<AppName>
    
    For Unix there is no *real* standard here. For example, Firefox uses:
    "~/.mozilla/firefox" which is a "~/.<appauthor>/<appname>"-type scheme.
    """
    if sys.platform.startswith("win"):
        if appauthor is None:
            raise AppDirsError("must specify 'appauthor' on Windows")
        const = roaming and "CSIDL_APPDATA" or "CSIDL_LOCAL_APPDATA"
        path = os.path.join(_get_win_folder(const), appauthor, appname)
    elif sys.platform == 'darwin':
        if os.uname()[-1] == 'i386':
            # Folder.FSFindFolder() **used to fail** with error -43
            # on x86. See Komodo bug 42669.
            #TODO: Update this to try FSFindFolder and fallback to this
            #      hardcoding for the specific failure mode.
            basepath = os.path.expanduser('~/Library/Application Support')
        else:
            from Carbon import Folder, Folders
            path = Folder.FSFindFolder(Folders.kUserDomain,
                                       Folders.kApplicationSupportFolderType,
                                       Folders.kDontCreateFolder)
            basepath = path.FSRefMakePath()
        path = os.path.join(basepath, appname)
    else:
        path = os.path.expanduser("~/." + appname.lower())
    if version:
        path = os.path.join(path, version)
    return path


def site_data_dir(appname, appauthor=None, version=None):
    """Return full path to the user-shared data dir for this application.
    
        "appname" is the name of application.
        "appauthor" (only required and used on Windows) is the name of the
            appauthor or distributing body for this application. Typically
            it is the owning company name.
        "version" is an optional version path element to append to the
            path. You might want to use this if you want multiple versions
            of your app to be able to run independently. If used, this
            would typically be "<major>.<minor>".
    
    Typical user data directories are:
        Mac OS X:   /Library/Application Support/<AppName>
        Unix:       /etc/<appname>
        Win XP:     C:\Documents and Settings\All Users\Application Data\<AppAuthor>\<AppName>
        Vista:      (Fail! "C:\ProgramData" is a hidden *system* directory on Vista.)
        Win 7:      C:\ProgramData\<AppAuthor>\<AppName>   # Hidden, but writeable on Win 7.
    
    Warning: Do not use this on Windows. See the Vista-Fail note above for why.
    """
    if sys.platform.startswith("win"):
        if appauthor is None:
            raise AppDirsError("must specify 'appauthor' on Windows")
        path = os.path.join(_get_win_folder("CSIDL_COMMON_APPDATA"),
                            appauthor, appname)
    elif sys.platform == 'darwin':
        if os.uname()[-1] == 'i386':
            # Folder.FSFindFolder() **used to fail** with error -43
            # on x86. See Komodo bug 42669.
            #TODO: Update this to try FSFindFolder and fallback to this
            #      hardcoding for the specific failure mode.
            basepath = os.path.expanduser('/Library/Application Support')
        else:
            from Carbon import Folder, Folders
            path = Folder.FSFindFolder(Folders.kLocalDomain,
                                       Folders.kApplicationSupportFolderType,
                                       Folders.kDontCreateFolder)
            basepath = os.path.join(path.FSRefMakePath(), appname)
        path = os.path.join(basepath, appname)
    else:
        path = "/etc/"+appname.lower()
    if version:
        path = os.path.join(path, version)
    return path


def user_cache_dir(appname, appauthor=None, version=None):
    r"""Return full path to the user-specific cache dir for this application.
    
        "appname" is the name of application.
        "appauthor" (only required and used on Windows) is the name of the
            appauthor or distributing body for this application. Typically
            it is the owning company name.
        "version" is an optional version path element to append to the
            path. You might want to use this if you want multiple versions
            of your app to be able to run independently. If used, this
            would typically be "<major>.<minor>".
    
    Typical user cache directories are:
        Mac OS X:   ~/Library/Caches/<AppName>
        Unix:       ~/.<appname>/cache
        Win XP:     C:\Documents and Settings\<username>\Local Settings\Application Data\<AppAuthor>\<AppName>
        Vista:      C:\Users\<username>\AppData\Local\<AppAuthor>\<AppName>

    For Unix there is no *real* standard here. This "cache" subdir is a
    suggestion from me.
    
    On Windows, note that this is identical to the non-roaming `user_data_dir`.
    Apps typically put cache data somewhere *under* the given dir here. Some
    examples:
        ...\Mozilla\Firefox\Profiles\<ProfileName>\Cache
        ...\Acme\SuperApp\1.0\Cache
    """
    if sys.platform.startswith("win"):
        if appauthor is None:
            raise AppDirsError("must specify 'appauthor' on Windows")
        path = os.path.join(_get_win_folder("CSIDL_LOCAL_APPDATA"),
                            appauthor, appname)
    elif sys.platform == 'darwin':
        if os.uname()[-1] == 'i386':
            # Folder.FSFindFolder() **used to fail** with error -43
            # on x86. See Komodo bug 42669.
            #TODO: Update this to try FSFindFolder and fallback to this
            #      hardcoding for the specific failure mode.
            basepath = os.path.expanduser('~/Library/Caches')
        else:
            from Carbon import Folder, Folders
            path = Folder.FSFindFolder(Folders.kUserDomain,
                                       Folders.kCachedDataFolderType,
                                       Folders.kDontCreateFolder)
            basepath = path.FSRefMakePath()
        path = os.path.join(basepath, appname)
    else:
        path = os.path.expanduser("~/.%s/cache" % appname.lower())
    if version:
        path = os.path.join(path, version)
    return path





#---- internal support stuff

def _get_win_folder_from_registry(csidl_name):
    """This is a fallback technique at best. I'm not sure if using the
    registry for this guarantees us the correct answer for all CSIDL_*
    names.
    """
    import _winreg
    
    shell_folder_name = {
        "CSIDL_APPDATA": "AppData",
        "CSIDL_COMMON_APPDATA": "Common AppData",
        "CSIDL_LOCAL_APPDATA": "Local AppData",
    }[csidl_name]

    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
    dir, type = _winreg.QueryValueEx(key, shell_folder_name)
    return dir

def _get_win_folder_with_pywin32(csidl_name):
    from win32com.shell import shellcon, shell
    dir = shell.SHGetFolderPath(0, getattr(shellcon, csidl_name), 0, 0)
    # Try to make this a unicode path because SHGetFolderPath does
    # not return unicode strings when there is unicode data in the
    # path.
    try:
        dir = unicode(dir)
        
        # Downgrade to short path name if have highbit chars. See
        # <http://bugs.activestate.com/show_bug.cgi?id=85099>.
        has_high_char = False
        for c in dir:
            if ord(c) > 255:
                has_high_char = True
                break
        if has_high_char:
            try:
                import win32api
                dir = win32api.GetShortPathName(dir)
            except ImportError:
                pass    
    except UnicodeError:
        pass
    return dir

def _get_win_folder_with_ctypes(csidl_name):
    import ctypes

    csidl_const = {
        "CSIDL_APPDATA": 26,
        "CSIDL_COMMON_APPDATA": 35,
        "CSIDL_LOCAL_APPDATA": 28,
    }[csidl_name]
    
    buf = ctypes.create_unicode_buffer(1024)
    ctypes.windll.shell32.SHGetFolderPathW(None, csidl_const, None, 0, buf)
    
    # Downgrade to short path name if have highbit chars. See
    # <http://bugs.activestate.com/show_bug.cgi?id=85099>.
    has_high_char = False
    for c in buf:
        if ord(c) > 255:
            has_high_char = True
            break
    if has_high_char:
        buf2 = ctypes.create_unicode_buffer(1024)
        if ctypes.windll.kernel32.GetShortPathNameW(buf.value, buf2, 1024):
            buf = buf2
    
    return buf.value

if sys.platform == "win32":
    try:
        import win32com.shell
        _get_win_folder = _get_win_folder_with_pywin32
    except ImportError:
        try:
            import ctypes
            _get_win_folder = _get_win_folder_with_ctypes
        except ImportError:
            _get_win_folder = _get_win_folder_from_registry



#---- self test code

if __name__ == "__main__":
    print("user data dir: %s" % user_data_dir("Komodo", "ActiveState"))
    print("site data dir: %s" % site_data_dir("Komodo", "ActiveState"))
    print("user cache dir: %s" % user_cache_dir("Komodo", "ActiveState"))

