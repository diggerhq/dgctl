python -m venv .venv
source .venv/bin/activate
pip install pgctl
pip install pyinstaller
pyinstaller src/dgctl/dgctl.py
