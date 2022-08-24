@echo off
python -m pyinstaller -w --name=interceptor --add-data="config.ini;." --noconfirm main.py
pause > nul