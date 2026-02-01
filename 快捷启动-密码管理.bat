@echo off
chcp 65001 >nul
cd /d "%~dp010_PasswordManager"
python password_manager.py
pause
