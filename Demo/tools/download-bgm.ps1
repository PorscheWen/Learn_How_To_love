# Download default Demo BGM (CC-BY from OpenGameArt). See assets/audio/CREDITS.md
param(
  [switch]$Force
)

$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$out = Join-Path $root 'assets\audio'
New-Item -ItemType Directory -Force -Path $out | Out-Null

$files = @{
  'warm.ogg'       = 'https://opengameart.org/sites/default/files/peaceful_intro.ogg'
  'calm.ogg'       = 'https://opengameart.org/sites/default/files/peaceatlast_piano.ogg'
  'tender.ogg'     = 'https://opengameart.org/sites/default/files/Thoughtful%20Piano%20Theme.ogg'
  'melancholy.ogg' = 'https://opengameart.org/sites/default/files/emotional_piano_solo.ogg'
}

$minBytes = 2048
$failed = @()

function Test-AudioFile([string]$Path) {
  return (Test-Path -LiteralPath $Path) -and ((Get-Item -LiteralPath $Path).Length -ge $minBytes)
}

foreach ($name in ($files.Keys | Sort-Object)) {
  $dest = Join-Path $out $name
  $tmp = Join-Path $out "$name.tmp"

  if (-not $Force -and (Test-AudioFile $dest)) {
    $kb = [math]::Round((Get-Item -LiteralPath $dest).Length / 1KB)
    Write-Host "Skip $name (already exists, ${kb} KB)"
    continue
  }

  Write-Host "Downloading $name ..."
  try {
    if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue }
    Invoke-WebRequest -Uri $files[$name] -OutFile $tmp -TimeoutSec 120

    if (-not (Test-Path -LiteralPath $tmp) -or (Get-Item -LiteralPath $tmp).Length -lt $minBytes) {
      throw "Download too small or missing: $name"
    }

    if (Test-Path -LiteralPath $dest) {
      try {
        Remove-Item -LiteralPath $dest -Force -ErrorAction Stop
      } catch {
        if (Test-AudioFile $dest) {
          Write-Warning "$name is in use; keeping existing file. Close the game/browser to update."
          Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
          continue
        }
        throw
      }
    }

    Move-Item -LiteralPath $tmp -Destination $dest -Force
    $kb = [math]::Round((Get-Item -LiteralPath $dest).Length / 1KB)
    Write-Host "  -> $kb KB"
  } catch {
    Write-Warning "Failed $name : $($_.Exception.Message)"
    if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue }
    if (Test-AudioFile $dest) {
      Write-Host "  (existing copy kept)"
    } else {
      $failed += $name
    }
  }
}

if ($failed.Count -gt 0) {
  Write-Host "Missing: $($failed -join ', ')" -ForegroundColor Red
  exit 1
}

Write-Host 'Done. Credits required — see assets/audio/CREDITS.md'
