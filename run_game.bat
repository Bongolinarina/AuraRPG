@echo off
chcp 65001 >nul
title AuraRPG Launcher

:: === Path to your main.py ===
set MAIN_PY="D:\Python Games\Aura RPG\scripts\main.py"

:: === Launch Python in a new CMD window ===
start "" cmd /k python %MAIN_PY%

:: Exit this launcher immediately
exit
