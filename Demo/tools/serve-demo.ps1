# Local HTTP server for Demo (required for BGM fetch + reliable Web Audio)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$demo = Split-Path -Parent $root
$port = 8765

Set-Location $demo

& (Join-Path $root 'deploy-audio.ps1')

Write-Host "Starting http://localhost:$port/ ..." -ForegroundColor Cyan
Start-Process "http://localhost:$port/"

python -m http.server $port
