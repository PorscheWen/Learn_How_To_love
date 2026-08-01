# Link Version2 assets into Renpy_game/game/assets
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$gameAssets = Join-Path $PSScriptRoot "..\game\assets" | Resolve-Path -ErrorAction SilentlyContinue
$target = Join-Path $root "assets"
$link = Join-Path (Split-Path -Parent $PSScriptRoot) "game\assets"
# Fix paths relative to Renpy_game
$renpyRoot = Split-Path -Parent $PSScriptRoot
if (-not $PSScriptRoot.EndsWith("tools")) {
    $renpyRoot = $PSScriptRoot
}
$renpyRoot = Split-Path -Parent $PSScriptRoot
$link = Join-Path $renpyRoot "game\assets"
$target = Join-Path (Split-Path -Parent $renpyRoot) "assets"

if (-not (Test-Path $target)) {
    Write-Error "Assets not found: $target"
    exit 1
}

if (Test-Path $link) {
    $item = Get-Item $link
    if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
        Write-Host "Assets junction already exists."
        exit 0
    }
    Remove-Item $link -Recurse -Force
}

cmd /c "mklink /J `"$link`" `"$target`""
if ($LASTEXITCODE -ne 0) {
    Write-Error "mklink failed"
    exit 1
}
Write-Host "Linked $link -> $target"
