@echo off
chcp 65001 >nul
cd /d "%~dp011_FileOrganizer"
python file_organizer.py
pause
