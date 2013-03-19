#!/usr/bin/env python

import sys
import os
from distutils.core import setup, Command
import appdirs

requires_list = []
try:
    import unittest2 as unittest
except ImportError:
    import unittest
else:
    if sys.version_info <= (2, 6):
        requires_list.append("unittest2")


class RunTests(Command):
    """New setup.py command to run all tests for the package.
    """
    description = "run all tests for the package"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        tests = unittest.TestLoader().discover('.')
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(tests)


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as inf:
        return "\n" + inf.read().replace("\r\n", "\n")


setup(name='appdirs',
    version=appdirs.__version__,
    description='A small Python module for determining appropriate " + \
        "platform-specific dirs, e.g. a "user data dir".',
    long_description=read('README.rst') + '\n' + read('CHANGES.rst'),
    cmdclass={'test': RunTests},
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
    requires=requires_list,
    keywords='application directory log cache user',
    author='Trent Mick',
    author_email='trentm@gmail.com',
    maintainer='Trent Mick; Sridhar Ratnakumar',
    maintainer_email='trentm@gmail.com; github@srid.name',
    url='http://github.com/ActiveState/appdirs',
    license='MIT',
    py_modules=["appdirs"],
)
