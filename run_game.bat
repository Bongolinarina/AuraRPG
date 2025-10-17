@echo off
chcp 65001 >nul
title AuraRPG Launcher

:: === Path to your main.py ===
set "MAIN_PY=D:\Python Games\Aura RPG\scripts\main.py"

echo [DEBUG] MAIN_PY set to "%MAIN_PY%"
echo [DEBUG] Checking if file exists...
if not exist "%MAIN_PY%" (
    echo [ERROR] main.py not found at "%MAIN_PY%"
    pause
    exit /b
)

:: Wait 1 second to ensure updates have finished
echo [DEBUG] Waiting 1 second before launching main.py...
timeout /t 1 /nobreak >nul

echo [DEBUG] Launching CMD to run Python script...
:: Launch in a new CMD window
start "" cmd /K "python "%MAIN_PY%""

echo [DEBUG] Launcher exiting...
exit
