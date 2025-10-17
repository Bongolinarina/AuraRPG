@echo off
chcp 65001 >nul
title AuraRPG Launcher

:: === Path to main.py ===
set MAIN_PY="D:\Python Games\Aura RPG\scripts\main.py"

:: === Launch Python in new CMD but keep it open after exit ===
start "" cmd /k python %MAIN_PY%
exit