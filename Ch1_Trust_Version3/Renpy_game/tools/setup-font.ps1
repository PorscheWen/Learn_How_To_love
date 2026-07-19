$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Dst = Join-Path $Root "game\SourceHanSansLite.ttf"
$Candidates = @(
    (Join-Path $PSScriptRoot "renpy-sdk\sdk-fonts\SourceHanSansLite.ttf"),
    (Join-Path $Root "..\..\Ch1_Trust_Version2\Renpy_game\game\SourceHanSansLite.ttf"),
    (Join-Path $Root "..\..\Ch1_Trust\Renpy_game\game\SourceHanSansLite.ttf")
)

foreach ($Src in $Candidates) {
    if (Test-Path $Src) {
        Copy-Item $Src $Dst -Force
        Write-Host "Font installed: $Dst"
        exit 0
    }
}

Write-Error "SourceHanSansLite.ttf not found. Install Ren'Py SDK first or place the font in game/."
exit 1
