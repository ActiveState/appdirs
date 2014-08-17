# HACKING 

## release

ensure correct version on CHANGES.md and appdirs.py, and:

```
python setup.py sdist register upload
```

## docker image

```
docker build -t appdirs .
```

