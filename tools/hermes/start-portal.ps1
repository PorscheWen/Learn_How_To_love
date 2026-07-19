# 啟動 Nous Portal（不自動開瀏覽器；請手動開 http://127.0.0.1:8780/）
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
python hermes.py setup --portal --no-browser
