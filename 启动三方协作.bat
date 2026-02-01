@echo off
title 三方协作系统 - 持续运行
color 0A

echo ============================================================
echo           三方协作自动化系统
echo      星星 + 铁血士 + Ollama
echo ============================================================
echo.
echo 系统将持续运行，只要电脑开机就会工作
echo 按 Ctrl+C 可以停止
echo.
echo 启动中...
echo.

cd /d G:\AI
python three_way_collaboration.py

pause
