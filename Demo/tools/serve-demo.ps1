# Local HTTP server for Demo (required for BGM fetch + reliable Web Audio)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$demo = Split-Path -Parent $root
$port = 8765

Set-Location $demo

& (Join-Path $root 'deploy-audio.ps1')

Write-Host "Starting http://localhost:$port/ (editor save API enabled) ..." -ForegroundColor Cyan
Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue |
  ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
$env:DEMO_PORT = "$port"
$env:DEMO_RESULT_PORT = "8769"
Start-Process "http://127.0.0.1:$port/game_editor.html"

python (Join-Path $root 'demo-server.py')
