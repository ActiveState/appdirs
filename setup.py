#!/usr/bin/env python
import sys
import os
import os.path
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
        test_modules = ["test.%s" % filename.replace('.py', '')
            for filename in os.listdir('test')
            if filename.endswith('.py') and filename.startswith('test_')]
        for mod in test_modules:
            __import__(mod)

        suite = unittest.TestSuite()
        for mod in [sys.modules[modname] for modname in test_modules]:
            suite.addTest(unittest.TestLoader().loadTestsFromModule(mod))
        unittest.TextTestRunner(verbosity=2).run(suite)


def read(fname):
    inf = open(os.path.join(os.path.dirname(__file__), fname))
    out = "\n" + inf.read().replace("\r\n", "\n")
    inf.close()
    return out


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
