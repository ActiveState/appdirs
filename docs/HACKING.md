# HACKING 

## release

ensure correct version in CHANGES.md and appdirs.py, and:

```
python setup.py sdist bdist_wheel
python -m twine upload dist/*
```

## docker image

```
docker build -t appdirs .
```
