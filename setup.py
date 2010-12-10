#!/usr/bin/env python

import sys
import os
from setuptools import setup, find_packages



_top_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_top_dir, "lib"))
try:
    import appdirs
finally:
    del sys.path[0]
README = open(os.path.join(_top_dir, 'README.rst')).read()
CHANGES = open(os.path.join(_top_dir, 'CHANGES.rst')).read()

setup(name='appdirs',
    version=appdirs.__version__,
    description='A small Python module for determining appropriate platform-specific dirs, e.g. a "user data dir".',
    long_description=README + '\n' + CHANGES,
    classifiers=[c.strip() for c in """
        Development Status :: 4 - Beta
        Intended Audience :: Developers
        License :: OSI Approved :: MIT License
        Operating System :: OS Independent
        Programming Language :: Python :: 2
        Programming Language :: Python :: 2.4
        Programming Language :: Python :: 2.5
        Programming Language :: Python :: 2.6
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.1
        Programming Language :: Python :: 3.2
        Topic :: Software Development :: Libraries :: Python Modules
        """.split('\n') if c.strip()],
    keywords='application directory log cache user',
    author='Trent Mick',
    author_email='trentm@gmail.com',
    maintainer='Trent Mick; Sridhar Ratnakumar',
    maintainer_email='trentm@gmail.com; github@srid.name',
    url='http://github.com/ActiveState/appdirs',
    license='MIT',
    py_modules=["appdirs"],
    package_dir={"": "lib"},
    include_package_data=True,
    zip_safe=False,
)
