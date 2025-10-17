@echo off
chcp 65001 >nul
title AuraRPG Launcher

:: Absolute path to main.py
set "MAIN_PY=D:\Python Games\Aura RPG\scripts\main.py"

:: Launch main.py in the current CMD window
python "%MAIN_PY%"

:: Exit CMD after main.py finishes
exit
