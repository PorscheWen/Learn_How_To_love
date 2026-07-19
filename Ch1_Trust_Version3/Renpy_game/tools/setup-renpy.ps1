param(
    [string]$Version = "8.3.7"
)

$ErrorActionPreference = "Stop"
$SdkDir = Join-Path $PSScriptRoot "renpy-sdk"
$RenpyExe = Join-Path $SdkDir "renpy.exe"

if (Test-Path $RenpyExe) {
    Write-Host "Ren'Py SDK 已存在：$RenpyExe"
    exit 0
}

$Url = "https://www.renpy.org/dl/$Version/renpy-$Version-sdk.7z.exe"
$Installer = Join-Path $env:TEMP "renpy-$Version-sdk.7z.exe"

Write-Host "下載 Ren'Py SDK $Version..."
Invoke-WebRequest -Uri $Url -OutFile $Installer -UseBasicParsing

New-Item -ItemType Directory -Force -Path $SdkDir | Out-Null
$process = Start-Process `
    -FilePath $Installer `
    -ArgumentList "-o$SdkDir", "-y" `
    -Wait `
    -PassThru `
    -NoNewWindow

if ($process.ExitCode -ne 0) {
    throw "Ren'Py SDK 解壓失敗，exit code $($process.ExitCode)"
}

$nested = Get-ChildItem $SdkDir -Directory -Filter "renpy-*" |
    Select-Object -First 1
if ($nested -and -not (Test-Path $RenpyExe)) {
    Get-ChildItem $nested.FullName | Move-Item -Destination $SdkDir -Force
    Remove-Item $nested.FullName -Recurse -Force
}

if (-not (Test-Path $RenpyExe)) {
    throw "找不到 renpy.exe，請手動安裝 SDK 到 $SdkDir"
}

Remove-Item $Installer -Force -ErrorAction SilentlyContinue
Write-Host "Ren'Py SDK 就緒：$RenpyExe"
