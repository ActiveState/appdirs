FROM activestate/activepython:2.7

WORKDIR /app
ADD . /app
RUN python setup.py install
RUN python -m appdirs

# For Python3 compact
RUN apt-get -y update && apt-get -y install python3-setuptools && apt-get -y clean
RUN python3 setup.py install
RUN python3 -m appdirs
