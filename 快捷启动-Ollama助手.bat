@echo off
chcp 65001 >nul
cd /d "%~dp0OllamaAssistant"
python ollama_assistant.py
pause
