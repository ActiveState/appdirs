# The Problem

What directory should your app use for storing user data? If running on Mac OS X, you
should use:

    ~/Library/Application Support/<AppName>

If on Windows (at least English Win XP) that should be:

    C:\Documents and Settings\<User>\Application Data\Local Settings\<AppAuthor>\<AppName>

or possibly:

    C:\Documents and Settings\<User>\Application Data\<AppAuthor>\<AppName>

for [roaming profiles](http://technet.microsoft.com/en-us/library/cc766489(WS.10).aspx) but
that is another story.

On Linux (and other Unices) the dir is typically:

    ~/.<appname>     # note AppName was lowercased


# `appdirs`

This kind of thing is what the `appdirs` module is for. `appdirs`:

- will tell you an appropriate user data dir (`user_data_dir`)
- will tell you an appropriate user caches dir (`user_caches_dir`)
- will tell you an appropriate site data dir (`site_data_dir`)
- is a single module so other Python packages can include their own private copy
- is slightly opinionated on the directory names used (especially on Linux/Unix
  where standards for these dirs don't really exist, AFAIK)




