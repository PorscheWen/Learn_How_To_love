@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo 啟動遊戲內容編輯器…
where python >nul 2>&1
if errorlevel 1 (
  echo 錯誤：未找到 Python 3，請先安裝 Python。
  pause
  exit /b 1
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8765 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1
start "demo-server" /MIN cmd /c "cd /d ""%~dp0"" && set DEMO_PORT=8765 && set DEMO_RESULT_PORT=8769 && python tools\demo-server.py"

echo 等待伺服器啟動…
ping 127.0.0.1 -n 4 >nul

powershell -NoProfile -Command "try { $r = Invoke-RestMethod -Uri 'http://127.0.0.1:8765/api/editor' -TimeoutSec 5; if (-not $r.save) { exit 1 } } catch { exit 1 }"
if errorlevel 1 (
  echo.
  echo [錯誤] demo-server 未正常啟動。
  echo 請手動執行：cd /d "%~dp0" ^&^& python tools\demo-server.py
  pause
  exit /b 1
)

start "" "http://127.0.0.1:8765/game_editor.html"
echo.
echo 編輯器已開啟：http://127.0.0.1:8765/game_editor.html
echo 儲存後伺服器會自動重啟，可繼續編輯。
pause
