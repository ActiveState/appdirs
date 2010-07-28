# appdirs Changelog

## appdirs 1.1.0 (not yet released)

- Add `roaming` option to `user_data_dir()` (for use on Windows only) and change
  the default `user_data_dir` behaviour to use a *non*-roaming profile dir
  (`CSIDL_LOCAL_APPDATA` instead of `CSIDL_APPDATA`). Why? Because a large
  roaming profile can cause login speed issues. The "only syncs on logout"
  behaviour can cause surprises in appdata info.


## appdirs 1.0.1 (never released)

Started this changelog 27 July 2010. Before that this module originated in the
[Komodo](http://www.activestate.com/komodo) product as `applib.py` and then as
[applib/location.py](http://github.com/ActiveState/applib/blob/master/applib/location.py)
(used by PyPM in [ActivePython](http://www.activestate.com/activepython)). This
is basically a fork of applib.py 1.0.1 and applib/location.py 1.0.1.

