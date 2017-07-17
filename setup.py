#!/usr/bin/env python
import sys
import os
import os.path
# appdirs is a dependency of setuptools, so allow installing without it.
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import ast

tests_require = []
if sys.version_info < (2, 7):
    tests_require.append("unittest2")

if sys.platform == "win32":
    test_suite = 'test.test_api_win32'
elif sys.platform == "darwin":
    test_suite = 'test.test_api_darwin'
else:
    test_suite = 'test.test_api_linux'


def read(fname):
    inf = open(os.path.join(os.path.dirname(__file__), fname))
    out = "\n" + inf.read().replace("\r\n", "\n")
    inf.close()
    return out


# Do not import `appdirs` yet, lest we import some random version on sys.path.
for line in read("appdirs.py").splitlines():
    if line.startswith("__version__"):
        version = ast.literal_eval(line.split("=", 1)[1].strip())
        break


setup(
    name='appdirs',
    version=version,
    description='A small Python module for determining appropriate ' + \
        'platform-specific dirs, e.g. a "user data dir".',
    long_description=read('README.rst') + '\n' + read('CHANGES.rst'),
    classifiers=[c.strip() for c in """
        Development Status :: 5 - Production/Stable
        Intended Audience :: Developers
        License :: OSI Approved :: MIT License
        Operating System :: OS Independent
        Programming Language :: Python :: 2
        Programming Language :: Python :: 2.6
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.2
        Programming Language :: Python :: 3.3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: 3.6
        Programming Language :: Python :: Implementation :: PyPy
        Programming Language :: Python :: Implementation :: CPython
        Topic :: Software Development :: Libraries :: Python Modules
        """.split('\n') if c.strip()],
    test_suite=test_suite,
    tests_require=tests_require,
    keywords='application directory log cache user',
    author='Trent Mick',
    author_email='trentm@gmail.com',
    maintainer='Trent Mick; Sridhar Ratnakumar; Jeff Rouse',
    maintainer_email='trentm@gmail.com; github@srid.name; jr@its.to',
    url='http://github.com/ActiveState/appdirs',
    license='MIT',
    py_modules=["appdirs"],
)
