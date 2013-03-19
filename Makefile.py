# This is a Makefile for the `mk` tool. Install it using,
#
#    pip install which mk


import sys
import os
from os.path import join, dirname, normpath, abspath, exists, basename, expanduser
import re
from glob import glob
import codecs
import webbrowser

import mklib
assert mklib.__version_info__ >= (0,7,2)  # for `mklib.mk`
from mklib.common import MkError
from mklib import Task, mk
from mklib import sh


class bugs(Task):
    """open bug/issues page"""
    def make(self):
        webbrowser.open("http://github.com/ActiveState/appdirs/issues")

class site(Task):
    """open project page"""
    def make(self):
        webbrowser.open("http://github.com/ActiveState/appdirs")

class pypi(Task):
    """open project page"""
    def make(self):
        webbrowser.open("http://pypi.python.org/pypi/appdirs/")

class cut_a_release(Task):
    """automate the steps for cutting a release

    See <http://github.com/trentm/eol/blob/master/docs/devguide.md>
    for details.
    """
    proj_name = "appdirs"
    version_py_path = "appdirs.py"
    version_module = "appdirs"

    # XXX: this needs to be changed from .md to .rst format
    _changes_parser = re.compile(r'^## %s (?P<ver>[\d\.abc]+)'
        r'(?P<nyr>\s+\(not yet released\))?'
        r'(?P<body>.*?)(?=^##|\Z)' % proj_name, re.M | re.S)

    def make(self):
        DRY_RUN = False
        version = self._get_version()

        # Confirm
        if not DRY_RUN:
            answer = query_yes_no("* * *\n"
                "Are you sure you want cut a %s release?\n"
                "This will involved commits and a release to pypi." % version,
                default="no")
            if answer != "yes":
                self.log.info("user abort")
                return
            print "* * *"
        self.log.info("cutting a %s release", version)

        # Checks: Ensure there is a section in changes for this version.
        changes_path = join(self.dir, "CHANGES.rst")
        changes_txt = changes_txt_before = codecs.open(changes_path, 'r', 'utf-8').read()
        raise NotImplementedError('_changes_parser: change me to .rst')
        changes_sections = self._changes_parser.findall(changes_txt)
        top_ver = changes_sections[0][0]
        if top_ver != version:
            raise MkError("top section in `CHANGES.rst' is for "
                "version %r, expected version %r: aborting"
                % (top_ver, version))
        top_nyr = changes_sections[0][1]
        if not top_nyr:
            answer = query_yes_no("\n* * *\n"
                "The top section in `CHANGES.rst' doesn't have the expected\n"
                "'(not yet released)' marker. Has this been released already?",
                default="yes")
            if answer != "no":
                self.log.info("abort")
                return
            print "* * *"
        top_body = changes_sections[0][2]
        if top_body.strip() == "(nothing yet)":
            raise MkError("top section body is `(nothing yet)': it looks like "
                "nothing has been added to this release")

        # Commits to prepare release.
        changes_txt = changes_txt.replace(" (not yet released)", "", 1)
        if not DRY_RUN and changes_txt != changes_txt_before:
            self.log.info("prepare `CHANGES.rst' for release")
            f = codecs.open(changes_path, 'w', 'utf-8')
            f.write(changes_txt)
            f.close()
            sh.run('git commit %s -m "prepare for %s release"'
                % (changes_path, version), self.log.debug)

        # Tag version and push.
        curr_tags = set(t for t in _capture_stdout(["git", "tag", "-l"]).split('\n') if t)
        if not DRY_RUN and version not in curr_tags:
            self.log.info("tag the release")
            sh.run('git tag -a "%s" -m "version %s"' % (version, version),
                self.log.debug)
            sh.run('git push --tags', self.log.debug)

        # Release to PyPI.
        self.log.info("release to pypi")
        if not DRY_RUN:
            mk("pypi_upload")

        # Commits to prepare for future dev and push.
        next_version = self._get_next_version(version)
        self.log.info("prepare for future dev (version %s)", next_version)
        marker = "## %s %s\n" % (self.proj_name, version)
        if marker not in changes_txt:
            raise MkError("couldn't find `%s' marker in `%s' "
                "content: can't prep for subsequent dev" % (marker, changes_path))
        changes_txt = changes_txt.replace("## %s %s\n" % (self.proj_name, version),
            "## %s %s (not yet released)\n\n(nothing yet)\n\n## %s %s\n" % (
                self.proj_name, next_version, self.proj_name, version))
        if not DRY_RUN:
            f = codecs.open(changes_path, 'w', 'utf-8')
            f.write(changes_txt)
            f.close()

        ver_path = join(self.dir, normpath(self.version_py_path))
        ver_content = codecs.open(ver_path, 'r', 'utf-8').read()
        version_tuple = self._tuple_from_version(version)
        next_version_tuple = self._tuple_from_version(next_version)
        marker = "__version_info__ = %r" % (version_tuple,)
        if marker not in ver_content:
            raise MkError("couldn't find `%s' version marker in `%s' "
                "content: can't prep for subsequent dev" % (marker, ver_path))
        ver_content = ver_content.replace(marker,
            "__version_info__ = %r" % (next_version_tuple,))
        if not DRY_RUN:
            f = codecs.open(ver_path, 'w', 'utf-8')
            f.write(ver_content)
            f.close()

        if not DRY_RUN:
            sh.run('git commit %s %s -m "prep for future dev"' % (
                changes_path, ver_path))
            sh.run('git push')

    def _tuple_from_version(self, version):
        def _intify(s):
            try:
                return int(s)
            except ValueError:
                return s
        return tuple(_intify(b) for b in version.split('.'))

    def _get_next_version(self, version):
        last_bit = version.rsplit('.', 1)[-1]
        try:
            last_bit = int(last_bit)
        except ValueError: # e.g. "1a2"
            last_bit = int(re.split('[abc]', last_bit, 1)[-1])
        return version[:-len(str(last_bit))] + str(last_bit + 1)

    def _get_version(self):
        try:
            mod = __import__(self.version_module)
            return mod.__version__
        finally:
            del sys.path[0]


class clean(Task):
    """Clean generated files and dirs."""
    def make(self):
        patterns = [
            "dist",
            "build",
            "MANIFEST",
            "*.pyc",
        ]
        for pattern in patterns:
            p = join(self.dir, pattern)
            for path in glob(p):
                sh.rm(path, log=self.log)

class sdist(Task):
    """python setup.py sdist"""
    def make(self):
        sh.run_in_dir("%spython setup.py sdist --formats zip"
                        % _setup_command_prefix(),
                      self.dir, self.log.debug)

class pypi_upload(Task):
    """Upload release to pypi."""
    def make(self):
        sh.run_in_dir("%spython setup.py sdist --formats zip upload"
                % _setup_command_prefix(),
            self.dir, self.log.debug)

        url = "http://pypi.python.org/pypi/appdirs/"
        import webbrowser
        webbrowser.open_new(url)

class tox(Task):
    """Test on all available Python versions using tox"""
    def make(self):
        sh.run("python toxbootstrap.py")

class test(Task):
    """Run all tests (except known failures)."""
    def make(self):
        for ver, python in self._gen_pythons():
            if ver < (2,3):
                # Don't support Python < 2.3.
                continue
            #elif ver >= (3, 0):
            #    # Don't yet support Python 3.
            #    continue
            ver_str = "%s.%s" % ver
            print "-- test with Python %s (%s)" % (ver_str, python)
            assert ' ' not in python
            sh.run("%s setup.py test" % python)

    def _python_ver_from_python(self, python):
        assert ' ' not in python
        o = os.popen('''%s -c "import sys; print(sys.version)"''' % python)
        ver_str = o.read().strip()
        ver_bits = re.split("\.|[^\d]", ver_str, 2)[:2]
        ver = tuple(map(int, ver_bits))
        return ver

    def _gen_python_names(self):
        yield "python"
        for ver in [(2,4), (2,5), (2,6), (2,7), (3,0), (3,1)]:
            yield "python%d.%d" % ver
            if sys.platform == "win32":
                yield "python%d%d" % ver

    def _gen_pythons(self):
        import which  # `pypm|pip install which`
        python_from_ver = {}
        for name in self._gen_python_names():
            for python in which.whichall(name):
                ver = self._python_ver_from_python(python)
                if ver not in python_from_ver:
                    python_from_ver[ver] = python
        for ver, python in sorted(python_from_ver.items()):
            yield ver, python




#---- internal support stuff

## {{{ http://code.activestate.com/recipes/577058/ (r2)
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":"yes",   "y":"yes",  "ye":"yes",
             "no":"no",     "n":"no"}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")
## end of http://code.activestate.com/recipes/577058/ }}}


def _setup_command_prefix():
    prefix = ""
    if sys.platform == "darwin":
        # http://forums.macosxhints.com/archive/index.php/t-43243.html
        # This is an Apple customization to `tar` to avoid creating
        # '._foo' files for extended-attributes for archived files.
        prefix = "COPY_EXTENDED_ATTRIBUTES_DISABLE=1 "
    return prefix

def _capture_stdout(argv):
    import subprocess
    p = subprocess.Popen(argv, stdout=subprocess.PIPE)
    return p.communicate()[0]
