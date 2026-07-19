@echo off
chcp 65001 >nul
cd /d "%~dp0"

set "RENPY=%~dp0tools\renpy-sdk\renpy.exe"
set "V2_RENPY=%~dp0..\..\Ch1_Trust_Version2\Renpy_game\tools\renpy-sdk\renpy.exe"
set "CH1_RENPY=%~dp0..\..\Ch1_Trust\Renpy_game\tools\renpy-sdk\renpy.exe"

if not exist "%RENPY%" (
    if exist "%V2_RENPY%" (
        set "RENPY=%V2_RENPY%"
    ) else if exist "%CH1_RENPY%" (
        set "RENPY=%CH1_RENPY%"
    ) else (
        echo 第一次執行：正在準備 Ren'Py SDK...
        powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\setup-renpy.ps1"
        if errorlevel 1 (
            echo Ren'Py SDK 安裝失敗。
            pause
            exit /b 1
        )
        set "RENPY=%~dp0tools\renpy-sdk\renpy.exe"
    )
)

if not exist "%RENPY%" (
    echo 找不到 renpy.exe：%RENPY%
    pause
    exit /b 1
)

set "FONT=%~dp0game\SourceHanSansLite.ttf"
if not exist "%FONT%" (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\setup-font.ps1"
    if errorlevel 1 (
        echo 找不到 SourceHanSansLite.ttf。
        pause
        exit /b 1
    )
)

echo 啟動 Learn How to Love｜Version3 S01...
start "" "%RENPY%" "%~dp0."
