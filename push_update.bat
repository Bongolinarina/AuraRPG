@echo off
echo -------------------------------
echo Git Auto Push for AuraRPG
echo -------------------------------
cd /d "D:\Python Games\Aura RPG"

:: Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo Git is not installed or not in PATH!
    pause
    exit /b
)

:: Ask for commit message
set /p message="Enter commit message: "

:: Stage all changes
git add .

:: Commit with the message
git commit -m "%message%"

:: Pull latest changes to avoid conflicts
git pull origin main --rebase

:: Push to GitHub
git push origin main

echo -------------------------------
echo Push complete!
pause
