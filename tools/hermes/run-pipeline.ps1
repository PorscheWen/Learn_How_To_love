# Hermes 完整管線：SDK 寫碼 + 測試（需 CURSOR_API_KEY）
param(
    [Parameter(Mandatory = $true)]
    [string]$Job
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
            [Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), "Process")
        }
    }
}

python hermes.py pipeline --job $Job
exit $LASTEXITCODE
