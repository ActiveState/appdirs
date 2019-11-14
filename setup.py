#!/usr/bin/env python
import os
# appdirs is a dependency of setuptools, so allow installing without it.
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import ast

current_dir = os.path.dirname(__file__)
def read(fname):
    inf = open(os.path.join(current_dir, fname), "rt", encoding="utf-8")
    out = "\n" + inf.read().replace("\r\n", "\n")
    inf.close()
    return out

if __name__ == "__main__":
    # Do not import `appdirs` yet, lest we import some random version on sys.path.
    for line in read("appdirs.py").splitlines():
        if line.startswith("__version__"):
            version = ast.literal_eval(line.split("=", 1)[1].strip())
            break


    setup(version=version)
