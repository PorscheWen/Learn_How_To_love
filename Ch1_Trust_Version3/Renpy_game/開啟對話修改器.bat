@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Starting dialogue editor...
python tools\dialogue_editor\server.py
if errorlevel 1 (
  echo.
  echo Failed. Ensure Python is on PATH.
  pause
)
