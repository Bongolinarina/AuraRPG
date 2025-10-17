@echo off
chcp 65001 >nul
title AuraRPG Launcher

:: Path to main.py
set "MAIN_PY=D:\Python Games\Aura RPG\scripts\main.py"

echo [DEBUG] Waiting 1 second before launching main.py...
timeout /t 1 /nobreak >nul

echo [DEBUG] Launching main.py...
:: /K keeps the window open
start "" cmd /K python "%MAIN_PY%"

echo [DEBUG] Launcher exiting...
exit
