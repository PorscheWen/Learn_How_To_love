# Bump ?v= cache query on css/js in index.html (run before each game launch)
$ErrorActionPreference = 'Stop'
$demo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$html = Join-Path $demo 'index.html'

if (-not (Test-Path -LiteralPath $html)) {
    Write-Error "index.html not found: $html"
    exit 1
}

$version = Get-Date -Format 'yyyyMMddHHmmss'
$content = [System.IO.File]::ReadAllText($html, [System.Text.Encoding]::UTF8)
$newContent = [regex]::Replace($content, '\?v=[^"''\s>]+', "?v=$version")

if ($newContent -eq $content) {
    Write-Warning 'No ?v= cache params found in index.html'
} else {
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText($html, $newContent, $utf8NoBom)
}

Write-Output $version
