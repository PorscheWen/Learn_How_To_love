# Copy SourceHanSansLite.ttf into game/ for Chinese text
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Dst = Join-Path $Root "game\SourceHanSansLite.ttf"
$Src = Join-Path $PSScriptRoot "renpy-sdk\sdk-fonts\SourceHanSansLite.ttf"

if (-not (Test-Path $Src)) { throw "Font not found: $Src" }
Copy-Item $Src $Dst -Force
Write-Host "Font installed: $Dst"
