@echo off
chcp 65001 >nul
title AuraRPG Launcher

:: === Path to your main.py ===
set MAIN_PY="D:\Python Games\Aura RPG\main.py"

:: === Launch Python in a new window ===
start "" python %MAIN_PY%

:: Exit this window immediately
exit
