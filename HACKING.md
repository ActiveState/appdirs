# HACKING 

## release

ensure correct version on CHANGES.md and appdirs.py, and:

```
python setup.py sdist bdist_wheel register upload
```

## docker image

```
docker build -t appdirs .
```

