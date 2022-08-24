@echo off
python -m pyinstaller -w --name=interceptor --add-data="config.ini;." --noconfirm main.py
7z a -r -y ./dist/interceptor.7z ./dist/interceptor/*.*
pause > nul