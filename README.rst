.. role:: python(code)
   :language: python

.. role:: bash(code)
   :language: bash

.. image:: https://secure.travis-ci.org/ActiveState/appdirs.png
    :target: https://travis-ci.org/ActiveState/appdirs

the problem
===========

What directory should your app use for storing user data? If running on macOS, you
should use::

    ~/Library/Application Support/<AppName>

If on Windows (at least English Win XP) that should be::

    C:\Documents and Settings\<User>\Application Data\Local Settings\<AppAuthor>\<AppName>

or possibly::

    C:\Documents and Settings\<User>\Application Data\<AppAuthor>\<AppName>

for `roaming profiles <https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-vista/cc766489(v=ws.10)>`_ but that is another story.

On Linux (and other Unices) the dir, according to the `XDG
spec <https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html>`_, is::

    ~/.local/share/<AppName>


``appdirs`` to the rescue
=========================

This kind of thing is what the ``appdirs`` module is for. ``appdirs`` will
help you choose the appropriate directory:

+-----------------------------------+-----------------------------+-----------------------------+
| Bash Shell Variable and           | Use Case                    | Return Type                 |
| ``appdirs`` Python Equivalent     |                             |                             |
+-----------------------------------+-----------------------------+-----------------------------+
| Bash: :bash:`$XDG_DATA_HOME`      | User-specific data files    | Single directory            |
|                                   |                             |                             |
| Python: :python:`user_data_dir`   |                             |                             |
+-----------------------------------+-----------------------------+-----------------------------+
| Bash: :bash:`$XDG_CONFIG_HOME`    | User-specific               | Single directory            |
|                                   | configuration files         |                             |
| Python: :python:`user_config_dir` |                             |                             |
+-----------------------------------+-----------------------------+-----------------------------+
| Bash: :bash:`$XDG_STATE_HOME`     | User-specific state data    | Single directory            |
|                                   |                             |                             |
| Python: N/A                       |                             |                             |
+-----------------------------------+-----------------------------+-----------------------------+
| Bash: :bash:`$XDG_DATA_DIRS`      | System data files           | Set of preference-ordered   |
|                                   |                             | base directories            |
| Python: :python:`site_data_dir`   |                             |                             |
+-----------------------------------+-----------------------------+-----------------------------+
| Bash: :bash:`$XDG_CONFIG_DIRS`    | System configuration files  | Set of preference-ordered   |
|                                   |                             | base directories            |
| Python: :python:`site_config_dir` |                             |                             |
+-----------------------------------+-----------------------------+-----------------------------+
| Bash: :bash:`$XDG_CACHE_HOME`     | User-specific non-essential | Single directory            |
|                                   |                             |                             |
| Python: N/A                       | (cached) data               |                             |
+-----------------------------------+-----------------------------+-----------------------------+
| Bash: :bash:`$XDG_RUNTIME_DIR`    | User-specific runtime files | Single directory            |
|                                   | and other file objects      |                             |
| Python: N/A                       |                             |                             |
+-----------------------------------+-----------------------------+-----------------------------+
| Bash: N/A                         | User-specific log files     | Single directory            |
|                                   |                             |                             |
| Python: :python:`user_log_dir`    |                             |                             |
+-----------------------------------+-----------------------------+-----------------------------+

and also:

- is a single module so other Python packages can include their own private copy
- is slightly opinionated on the directory names used. Look for "OPINION" in
  documentation and code for when an opinion is being applied.


some example output
===================

First:
------

.. code:: python

    >>> from appdirs import *
    >>> appname = "SuperApp"
    >>> appauthor = "Acme"


On macOS:
---------

+---------------------------------------------------+----------------------------------------------------------+
| Command                                           | Returns                                                  |
+---------------------------------------------------+----------------------------------------------------------+
| :python:`>>> user_data_dir(appname, appauthor)`   | ``'/Users/trentm/Library/Application Support/SuperApp'`` |
+---------------------------------------------------+----------------------------------------------------------+
| :python:`>>> site_data_dir(appname, appauthor)`   | ``'/Library/Application Support/SuperApp'``              |
+---------------------------------------------------+----------------------------------------------------------+
| :python:`>>> user_cache_dir(appname, appauthor)`  | ``'/Users/trentm/Library/Caches/SuperApp'``              |
+---------------------------------------------------+----------------------------------------------------------+
| :python:`>>> user_log_dir(appname, appauthor)`    | ``'/Users/trentm/Library/Logs/SuperApp'``                |
+---------------------------------------------------+----------------------------------------------------------+

On Windows 7:
-------------

+---------------------------------------------------------------+----------------------------------------------------------------+
| Command                                                       | Returns                                                        |
+---------------------------------------------------------------+----------------------------------------------------------------+
| :python:`>>> user_data_dir(appname, appauthor)`               | ``'C:\Users\trentm\AppData\Local\Acme\SuperApp'``              |
+---------------------------------------------------------------+----------------------------------------------------------------+
| :python:`>>> user_data_dir(appname, appauthor, roaming=True)` | ``'C:\Users\trentm\AppData\Roaming\Acme\SuperApp'``            |
+---------------------------------------------------------------+----------------------------------------------------------------+
| :python:`>>> user_cache_dir(appname, appauthor)`              | ``'C:\Users\trentm\AppData\Local\Acme\SuperApp\Cache'``        |
+---------------------------------------------------------------+----------------------------------------------------------------+
| :python:`>>> user_log_dir(appname, appauthor)`                | ``'C:\Users\trentm\AppData\Local\Acme\SuperApp\Logs'``         |
+---------------------------------------------------------------+----------------------------------------------------------------+

On Linux:
---------

+---------------------------------------------------------------------+-----------------------------------------------------+
| Command                                                             | Returns                                             |
+---------------------------------------------------------------------+-----------------------------------------------------+
| :python:`>>> user_data_dir(appname, appauthor)`                     | ``'/home/trentm/.local/share/SuperApp'``            |
+---------------------------------------------------------------------+-----------------------------------------------------+
| :python:`>>> site_data_dir(appname, appauthor)`                     | ``'/usr/local/share/SuperApp'``                     |
+---------------------------------------------------------------------+-----------------------------------------------------+
| :python:`>>> site_data_dir(appname, appauthor, multipath=True)`     | ``'/usr/local/share/SuperApp:/usr/share/SuperApp'`` |
+---------------------------------------------------------------------+-----------------------------------------------------+
| :python:`>>> user_cache_dir(appname, appauthor)`                    | ``'/home/trentm/.cache/SuperApp'``                  |
+---------------------------------------------------------------------+-----------------------------------------------------+
| :python:`>>> user_log_dir(appname, appauthor)`                      | ``'/home/trentm/.cache/SuperApp/log'``              |
+---------------------------------------------------------------------+-----------------------------------------------------+
| :python:`>>> user_config_dir(appname)`                              | ``'/home/trentm/.config/SuperApp'``                 |
+---------------------------------------------------------------------+-----------------------------------------------------+
| :python:`>>> site_config_dir(appname)`                              | ``'/etc/xdg/SuperApp'``                             |
+---------------------------------------------------------------------+-----------------------------------------------------+
| :python:`>>> os.environ['XDG_CONFIG_DIRS'] = '/etc:/usr/local/etc'` | ``'/etc/SuperApp:/usr/local/etc/SuperApp'``         |
|                                                                     |                                                     |
| :python:`>>> site_config_dir(appname, multipath=True)`              |                                                     |
+---------------------------------------------------------------------+-----------------------------------------------------+

``AppDirs`` for convenience
===========================

First:
------

.. code:: python

    >>> from appdirs import AppDirs
    >>> dirs = AppDirs("SuperApp", "Acme")

Then, e.g., on Linux:
---------------------

+------------------------------------+----------------------------------------------------------+
| Command                            | Returns                                                  |
+------------------------------------+----------------------------------------------------------+
| :python:`>>> dirs.user_data_dir`   | ``'/Users/trentm/Library/Application Support/SuperApp'`` |
+------------------------------------+----------------------------------------------------------+
| :python:`>>> dirs.site_data_dir`   | ``'/Library/Application Support/SuperApp'``              |
+------------------------------------+----------------------------------------------------------+
| :python:`>>> dirs.user_cache_dir`  | ``'/Users/trentm/Library/Caches/SuperApp'``              |
+------------------------------------+----------------------------------------------------------+
| :python:`>>> dirs.user_log_dir`    | ``'/Users/trentm/Library/Logs/SuperApp'``                |
+------------------------------------+----------------------------------------------------------+

Per-version isolation
=====================

If you have multiple versions of your app in use that you want to be
able to run side-by-side, then you may want version-isolation for these
dirs:

First:
------

.. code:: python

    >>> from appdirs import AppDirs
    >>> dirs = AppDirs("SuperApp", "Acme", version="1.0")

+------------------------------------+----------------------------------------------------------+
| Command                            | Returns                                                  |
+------------------------------------+----------------------------------------------------------+
| :python:`>>> dirs.user_data_dir`   | ``'/Users/trentm/Library/Application Support/SuperApp/1.0'`` |
+------------------------------------+----------------------------------------------------------+
| :python:`>>> dirs.site_data_dir`   | ``'/Library/Application Support/SuperApp/1.0'``              |
+------------------------------------+----------------------------------------------------------+
| :python:`>>> dirs.user_cache_dir`  | ``'/Users/trentm/Library/Caches/SuperApp/1.0'``              |
+------------------------------------+----------------------------------------------------------+
| :python:`>>> dirs.user_log_dir`    | ``'/Users/trentm/Library/Logs/SuperApp/1.0'``                |
+------------------------------------+----------------------------------------------------------+
