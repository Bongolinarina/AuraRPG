@echo off
chcp 65001 >nul
title AuraRPG Launcher

:: Path to main.py
set "MAIN_PY=D:\Python Games\Aura RPG\scripts\main.py"

echo Launching main.py...
start "" cmd /K python "%MAIN_PY%"

exit