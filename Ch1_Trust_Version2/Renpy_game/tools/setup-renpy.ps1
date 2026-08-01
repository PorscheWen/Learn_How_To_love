# 下載並解壓 Ren'Py SDK 到 tools/renpy-sdk/（僅首次需要，約 120 MB）
param(
    [string]$Version = "8.3.7"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$SdkDir = Join-Path $PSScriptRoot "renpy-sdk"
$RenpyExe = Join-Path $SdkDir "renpy.exe"

if (Test-Path $RenpyExe) {
    Write-Host "Ren'Py SDK 已存在: $RenpyExe"
    exit 0
}

$Url = "https://www.renpy.org/dl/$Version/renpy-$Version-sdk.7z.exe"
$Installer = Join-Path $env:TEMP "renpy-$Version-sdk.7z.exe"

Write-Host "下載 Ren'Py SDK $Version ..."
Write-Host "來源: $Url"
Invoke-WebRequest -Uri $Url -OutFile $Installer -UseBasicParsing

Write-Host "解壓到 $SdkDir ..."
New-Item -ItemType Directory -Force -Path $SdkDir | Out-Null

# 7z.exe 自解壓安裝檔：-o 輸出目錄，-y 全部確認
$proc = Start-Process -FilePath $Installer -ArgumentList "-o$SdkDir", "-y" -Wait -PassThru -NoNewWindow
if ($proc.ExitCode -ne 0) {
    throw "Ren'Py SDK 解壓失敗，exit code $($proc.ExitCode)"
}

# 解壓後通常在 renpy-8.x.x 子資料夾
$nested = Get-ChildItem $SdkDir -Directory -Filter "renpy-*" | Select-Object -First 1
if ($nested -and -not (Test-Path $RenpyExe)) {
    Get-ChildItem $nested.FullName | Move-Item -Destination $SdkDir -Force
    Remove-Item $nested.FullName -Recurse -Force -ErrorAction SilentlyContinue
}

if (-not (Test-Path $RenpyExe)) {
    throw "找不到 renpy.exe，請手動安裝 Ren'Py SDK 到 $SdkDir"
}

Remove-Item $Installer -Force -ErrorAction SilentlyContinue
Write-Host "Ren'Py SDK 就緒: $RenpyExe"
