Digger Control (dgctl)

# Install

```
python -m pip install dgctl
```

# Usage

Go to `environment-*` directory and execute following:

```
dgctl init
```

This command will create `backend.tf` file.

# Publish

```
rm -rf dist
python3 -m build
python3 -m twine upload --repository testpypi dist/*
```
