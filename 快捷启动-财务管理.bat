@echo off
chcp 65001 >nul
cd /d "%~dp007_PersonalFinanceManager"
start python app.py
echo ✅ 财务管理器已启动！
echo 📱 请在浏览器中访问: http://localhost:5000
pause
