#!/usr/bin/env python
# Copyright (c) 2010 ActiveState Software Inc.
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

"""The appdirs test suite entry point."""

import os
from os.path import exists, join, abspath, dirname, normpath
import sys
import logging

import testlib

log = logging.getLogger("test")
testdir_from_ns = {
    None: os.curdir,
}

def setup():
    top_dir = dirname(dirname(abspath(__file__)))
    lib_dir = join(top_dir, "lib")
    sys.path.insert(0, lib_dir)

if __name__ == "__main__":
    logging.basicConfig()
    setup()
    default_tags = []
    retval = testlib.harness(testdir_from_ns=testdir_from_ns,
                             default_tags=default_tags)
    sys.exit(retval)

