FROM activestate/activepython:2.7

WORKDIR /app
ADD . /app
RUN python setup.py install
RUN python -m appdirs
