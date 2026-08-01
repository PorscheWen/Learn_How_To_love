@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo Learn How to Love - RenPy Day1～3
echo.

set "RENPY=%~dp0tools\renpy-sdk\renpy.exe"
set "CH1_RENPY=%~dp0..\..\Ch1_Trust\Renpy_game\tools\renpy-sdk\renpy.exe"

if not exist "%RENPY%" (
    if exist "%CH1_RENPY%" (
        echo Using Ch1_Trust RenPy SDK...
        set "RENPY=%CH1_RENPY%"
    ) else (
        echo [1/2] Downloading RenPy SDK, first run only...
        if exist "%~dp0tools\setup-renpy.ps1" (
            powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\setup-renpy.ps1"
        ) else (
            echo Missing tools\setup-renpy.ps1
            echo Install Ren'Py from https://www.renpy.org/latest.html
            pause
            exit /b 1
        )
        if errorlevel 1 (
            echo Setup failed.
            pause
            exit /b 1
        )
        set "RENPY=%~dp0tools\renpy-sdk\renpy.exe"
    )
)

if not exist "%~dp0game\assets\bg\bg-street-night.png" (
    echo Linking assets...
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\link-assets.ps1"
)

echo Launching...
cd /d "%~dp0"
start "" "%RENPY%" .
echo.
echo Game window should open.
pause
