#!/usr/bin/env python
# Find the latest version of this script at:
#    http://github.com/srid/tox-bootstrap

import sys
import os
from os import path
from urllib import urlretrieve
import logging
import xmlrpclib
from subprocess import Popen, PIPE, check_call, CalledProcessError
import pkg_resources

logging.basicConfig(level=logging.INFO)


VIRTUALENVPY_URL = 'http://bitbucket.org/ianb/virtualenv/raw/tip/virtualenv.py'


def run(cmd, shell=True):
    """Run the given command in shell"""
    logging.info('Running command: %s', cmd)
    check_call(cmd, shell=shell)


def crun(cmd, shell=True):
    """Run the given command and return its output"""
    logging.info('Running command (for output): %s', cmd)
    p = Popen(cmd, stdout=PIPE, shell=shell)
    stdout, stderr = p.communicate()
    return stdout


def wget(url):
    """Download the given file to current directory"""
    logging.info('Downloading %s', url)
    localpath = path.join(path.abspath(os.getcwd()), path.basename(url))
    urlretrieve(url, localpath)


def has_script(venv, name):
    """Check if the virtualenv has the given script

    Looks for bin/$name (unix) or Scripts/$name.exe (windows) in the virtualenv
    """
    if sys.platform == 'win32':
        return any([path.exists(path.join(venv, 'Scripts', name)),
                    path.exists(path.join(venv, 'Scripts', name + '.exe'))])
    else:
        return path.exists(path.join(venv, 'bin', name))


def get_script_path(venv, name):
    """Return the full path to the script in virtualenv directory"""
    if sys.platform == 'win32':
        p = path.join(venv, 'Scripts', name)
        if not path.exists(p):
            p = path.join(venv, 'Scripts', name + '.exe')
    else:
        p = path.join(venv, 'bin', name)

    if not path.exists(p):
        raise NameError('cannot find a script named "{0}"'.format(name))

    return p


def get_tox_version(venv):
    """Return the installed version of tox"""
    py = get_script_path(venv, 'python')
    s = 'import tox,sys; sys.stdout.write(str(tox.__version__))'
    return crun('{0} -s -c "{1}"'.format(py, s))


def pypi_get_latest_version(pkgname):
    """Return the latest version of package from PyPI"""
    pypi = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    versions = pypi.package_releases('tox')
    assert versions
    versions.sort(key=pkg_resources.parse_version, reverse=True)
    return versions[0]


def cmdline(argv=None):
    os.chdir(path.abspath(path.dirname(__file__)))
    if not path.isdir('.tox'):
        os.mkdir('.tox')
    os.chdir('.tox')

    # create virtual environment
    if not path.isdir('toxinstall'):
        # get virtualenv.py
        if not path.isfile('virtualenv.py'):
            wget(VIRTUALENVPY_URL)
        assert path.isfile('virtualenv.py')

        # XXX: we use --no-site-packages because: if tox is installed in global
        # site-packages, then pip will not install it locally. ideal fix for
        # this should be to first look for tox in the global scripts/ directory
        run('python virtualenv.py --no-site-packages --distribute toxinstall')

    assert has_script('toxinstall', 'python')
    assert has_script('toxinstall', 'pip')

    # install/upgrade tox itself
    if any([
        not has_script('toxinstall', 'tox'),
        get_tox_version('toxinstall') != pypi_get_latest_version('tox')]):
        run('{0} install --upgrade --download-cache=pip-cache tox'.format(
                get_script_path('toxinstall', 'pip')))

    assert has_script('toxinstall', 'tox')
    tox_script = path.abspath(get_script_path('toxinstall', 'tox'))
    logging.info('tox is already installed at %s', tox_script)

    # Now run the locally-installed tox
    os.chdir('..')
    try:
        run([tox_script] + (argv or []), shell=False)
    except CalledProcessError as e:
        logging.error('tox exited with error code %d', e.returncode)
        sys.exit(e.returncode)


if __name__ == '__main__':
    cmdline(sys.argv[1:])
