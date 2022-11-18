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

Open pyproject.toml and bump version.

Build package:
```
rm -rf dist
python -m build
```

Test package on testpypi.org
```
python -m twine upload --repository testpypi dist/*
python -m pip install --index-url https://test.pypi.org/simple/ dgctl==0.1.4
```

Upload to official pip:
```
python -m twine upload dist/*
```
