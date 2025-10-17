@echo off
chcp 65001 >nul
title AuraRPG Launcher

:: === Path to your main.py ===
set MAIN_PY=D:\Python Games\Aura RPG\scripts\main.py

echo [DEBUG] MAIN_PY set to "%MAIN_PY%"
echo [DEBUG] Checking if file exists...
if not exist "%MAIN_PY%" (
    echo [ERROR] main.py not found at "%MAIN_PY%"
    pause
    exit /b
)

echo [DEBUG] Launching CMD to run Python script...
:: "" is window title; quotes around %MAIN_PY% handle spaces
start "" cmd /k (
    echo [DEBUG] Inside new CMD window
    python "%MAIN_PY%"
    if %errorlevel% neq 0 echo [ERROR] Python exited with code %errorlevel%
    pause
)

echo [DEBUG] Launcher exiting...
exit
