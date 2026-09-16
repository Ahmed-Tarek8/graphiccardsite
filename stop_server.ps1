$ErrorActionPreference = "SilentlyContinue"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$PidFile = Join-Path $Root ".graphiccardsite-server.pid"

if (Test-Path $PidFile) {
    $serverPid = (Get-Content $PidFile -Raw).Trim()
    if ($serverPid -match '^\d+$') {
        Stop-Process -Id ([int]$serverPid) -Force
    }
    Remove-Item $PidFile -Force
}

Write-Output "Graphics-card site server stopped."
