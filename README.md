# the problem

What directory should your app use for storing user data? If running on Mac OS X, you
should use:

    ~/Library/Application Support/<AppName>

If on Windows (at least English Win XP) that should be:

    C:\Documents and Settings\<User>\Application Data\Local Settings\<AppAuthor>\<AppName>

or possibly:

    C:\Documents and Settings\<User>\Application Data\<AppAuthor>\<AppName>

for [roaming profiles](http://bit.ly/9yl3b6) but that is another story.

On Linux (and other Unices) the dir is typically:

    ~/.<appname>     # note AppName was lowercased


# `appdirs` to the rescue

This kind of thing is what the `appdirs` module is for. `appdirs`:

- will tell you an appropriate user data dir (`user_data_dir`)
- will tell you an appropriate user cache dir (`user_cache_dir`)
- will tell you an appropriate site data dir (`site_data_dir`)
- is a single module so other Python packages can include their own private copy
- is slightly opinionated on the directory names used. Look for "OPINION" in
  documentation and code for when an opinion is being applied.


# some example output

On Mac OS X:

    >>> from appdirs import *
    >>> appname = "SuperApp"
    >>> appauthor = "Acme"
    >>> user_data_dir(appname, appauthor)
    '/Users/trentm/Library/Application Support/SuperApp'
    >>> site_data_dir(appname, appauthor)
    '/Library/Application Support/SuperApp'
    >>> user_cache_dir(appname, appauthor)
    '/Users/trentm/Library/Caches/SuperApp'

On Windows 7:

    >>> from appdirs import *
    >>> appname = "SuperApp"
    >>> appauthor = "Acme"
    >>> user_data_dir(appname, appauthor)
    'C:\\Users\\trentm\\AppData\\Local\\Acme\\SuperApp'
    >>> user_data_dir(appname, appauthor, roaming=True)
    'C:\\Users\\trentm\\AppData\\Roaming\\Acme\\SuperApp'
    >>> user_cache_dir(appname, appauthor)
    'C:\\Users\\trentm\\AppData\\Local\\Acme\\SuperApp'
    # Suggest at least "Cache" is appended to this to separate from
    # `user_data_dir`.
    >>> from os.path import join
    >>> join(user_cache_dir(appname, appauthor), "Cache")
    'C:\\Users\\trentm\\AppData\\Local\\Acme\\SuperApp\\Cache'

On Linux:

    >>> from appdirs import *
    >>> appname = "SuperApp"
    >>> appauthor = "Acme"
    >>> user_data_dir(appname, appauthor)
    '/home/trentm/.superapp
    >>> site_data_dir(appname, appauthor)
    '/etc/superapp'
    >>> user_cache_dir(appname, appauthor)
    '/home/trentm/.superapp/cache'


# `AppDirs` for convenience

    >>> from appdirs import AppDirs
    >>> dirs = AppDirs("SuperApp", "Acme")
    >>> dirs.user_data_dir
    '/Users/trentm/Library/Application Support/SuperApp'
    >>> dirs.site_data_dir
    '/Library/Application Support/SuperApp'
    >>> dirs.user_cache_dir
    '/Users/trentm/Library/Caches/SuperApp'

Note that the `AppDirs` default on Windows is to append "Cache" to the
`.user_cache_dir` as suggested above.

    
# Per-major-version isolation

    >>> from appdirs import AppDirs
    >>> dirs = AppDirs("SuperApp", "Acme", version="1.0")
    >>> dirs.user_data_dir
    '/Users/trentm/Library/Application Support/SuperApp/1.0'
    >>> dirs.site_data_dir
    '/Library/Application Support/SuperApp/1.0'
    >>> dirs.user_cache_dir
    '/Users/trentm/Library/Caches/SuperApp/1.0'

