@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo Learn How to Love — Demo
echo [1/3] 更新靜態資源快取版本…
for /f "delims=" %%V in ('powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\bump-cache.ps1"') do set "CACHE_V=%%V"
if not defined CACHE_V set "CACHE_V=0"
echo       快取版本 v=%CACHE_V%

echo [2/3] 部署背景音樂…
powershell -ExecutionPolicy Bypass -File "%~dp0tools\deploy-audio.ps1"
if errorlevel 1 echo 警告：BGM 下載失敗，將嘗試程序化音樂。

where python >nul 2>&1
if errorlevel 1 (
  echo [3/3] 未找到 Python，以 file 模式開啟（可能無聲，建議安裝 Python 3）
  start "" "%~dp0index.html"
  exit /b 0
)

echo [3/3] 啟動本機伺服器 http://localhost:8765/
start /B cmd /c "cd /d "%~dp0" && python -m http.server 8765"
timeout /t 2 /nobreak >nul
start "" "http://localhost:8765/?v=%CACHE_V%"

echo.
echo 遊戲已在瀏覽器開啟。關閉此視窗不會停止伺服器。
echo 若要停止：工作管理員結束 python.exe
pause
