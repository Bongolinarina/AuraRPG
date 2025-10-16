@echo off
echo Restoring AuraRPG from GitHub...

:: Change to the project folder
cd /d "D:\Python Games\Aura RPG"

:: Fetch latest from remote
git fetch origin

:: Reset local files to match remote exactly
git reset --hard origin/main

echo Restore complete!
pause
