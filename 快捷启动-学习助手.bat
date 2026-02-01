@echo off
chcp 65001 >nul
cd /d "%~dp006_SmartStudyAssistant"
start python app.py
echo ✅ 智能学习助手已启动！
echo 📱 请在浏览器中访问: http://localhost:5000
pause
