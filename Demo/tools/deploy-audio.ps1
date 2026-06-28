# Deploy Demo audio — download BGM only when missing; verify all assets
$ErrorActionPreference = 'Continue'
$demo = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $demo

Write-Host '=== LHTL Demo Audio Deploy ===' -ForegroundColor Cyan

$audioDir = Join-Path $root 'assets\audio'
$required = @('warm.ogg', 'calm.ogg', 'tender.ogg', 'melancholy.ogg')
$minBytes = 2048

function Test-AudioFile([string]$Path) {
  return (Test-Path -LiteralPath $Path) -and ((Get-Item -LiteralPath $Path).Length -ge $minBytes)
}

$missingBgm = @($required | Where-Object { -not (Test-AudioFile (Join-Path $audioDir $_)) })

if ($missingBgm.Count -gt 0) {
  Write-Host "Missing BGM: $($missingBgm -join ', ') — downloading ..."
  & (Join-Path $demo 'download-bgm.ps1')
  if ($LASTEXITCODE -ne 0) {
    Write-Warning 'BGM download incomplete (files may be locked if game is open).'
  }
} else {
  Write-Host 'BGM already present — skip download.'
}

if (Test-Path (Join-Path $demo 'download-dog-sfx.ps1')) {
  $dogDir = Join-Path $root 'assets\dog\sfx'
  $dogSample = Join-Path $dogDir 'puppy-whimper-a.wav'
  if (-not (Test-AudioFile $dogSample)) {
    Write-Host 'Missing dog SFX — downloading ...'
    & (Join-Path $demo 'download-dog-sfx.ps1')
  } else {
    Write-Host 'Dog SFX already present — skip download.'
  }
}

$ok = $true
foreach ($f in $required) {
  $p = Join-Path $audioDir $f
  if (Test-AudioFile $p) {
    $kb = [math]::Round((Get-Item -LiteralPath $p).Length / 1KB)
    Write-Host "[OK] $f ($kb KB)" -ForegroundColor Green
  } else {
    Write-Host "[MISSING] $f" -ForegroundColor Red
    $ok = $false
  }
}

$dogRequired = @(
  'puppy-whimper-a.wav', 'puppy-whimper-b.wav',
  'puppy-soft-a.wav', 'puppy-soft-b.wav',
  'puppy-sigh-a.wav', 'puppy-sigh-b.wav',
  'puppy-yip-a.ogg', 'puppy-yip-b.wav',
  'puppy-bark-a.wav', 'puppy-bark-b.wav',
  'puppy-excited-a.wav', 'puppy-excited-b.wav',
  'puppy-murmur-a.wav', 'puppy-murmur-b.wav',
  'puppy-whimper.wav', 'puppy-soft-whimper.wav', 'puppy-yip.ogg'
)
$dogDir = Join-Path $root 'assets\dog\sfx'
foreach ($f in $dogRequired) {
  $p = Join-Path $dogDir $f
  if (Test-Path -LiteralPath $p) {
    $kb = [math]::Round((Get-Item -LiteralPath $p).Length / 1KB)
    Write-Host "[OK] dog/sfx/$f ($kb KB)" -ForegroundColor Green
  } else {
    Write-Host "[MISSING] dog/sfx/$f" -ForegroundColor Red
    $ok = $false
  }
}

if (-not $ok) {
  Write-Host ''
  Write-Host 'Tip: close the browser game tab, then run play.bat again.' -ForegroundColor Yellow
  exit 1
}

Write-Host ''
Write-Host 'Audio deploy complete.' -ForegroundColor Cyan
