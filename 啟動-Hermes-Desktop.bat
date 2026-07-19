@echo off
set HERMES_HOME=%LOCALAPPDATA%\hermes
set HERMES_DESKTOP_CWD=%~dp0
start "" "%LOCALAPPDATA%\hermes\hermes-agent\apps\desktop\release\win-unpacked\Hermes.exe"
