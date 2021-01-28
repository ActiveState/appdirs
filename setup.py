#!/usr/bin/env python
from io import open
import os
# appdirs is a dependency of setuptools, so allow installing without it.
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import ast


def read(fname):
    inf = open(os.path.join(os.path.dirname(__file__), fname), encoding='utf8')
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
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='application directory log cache user',
    author='Trent Mick',
    author_email='trentm@gmail.com',
    maintainer='Jeff Rouse',
    maintainer_email='jr@its.to',
    url='https://github.com/ActiveState/appdirs',
    license='MIT',
    py_modules=["appdirs"],
)
