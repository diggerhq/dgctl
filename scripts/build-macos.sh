python3 -m venv .venv
source .venv/bin/activate
pip install dgctl
pip install pyinstaller
pyinstaller src/dgctl/dgctl.py
