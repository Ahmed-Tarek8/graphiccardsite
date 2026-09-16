param(
    [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Pythonw = Join-Path $Root ".venv\Scripts\pythonw.exe"
$ServerScript = Join-Path $Root "persistent_server.py"
$Url = "http://localhost:4181/"

function Test-GraphicCardSitePort {
    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $async = $client.BeginConnect("127.0.0.1", 4181, $null, $null)
        $connected = $async.AsyncWaitHandle.WaitOne(350)
        if (-not $connected) { return $false }
        $client.EndConnect($async)
        return $true
    }
    catch {
        return $false
    }
    finally {
        $client.Dispose()
    }
}

if (-not (Test-Path $Pythonw)) {
    throw "Python environment not found: $Pythonw"
}

if (-not (Test-Path $ServerScript)) {
    throw "Server script not found: $ServerScript"
}

if (-not (Test-GraphicCardSitePort)) {
    Start-Process `
        -FilePath $Pythonw `
        -ArgumentList @($ServerScript) `
        -WorkingDirectory $Root `
        -WindowStyle Hidden | Out-Null

    $ready = $false
    for ($attempt = 0; $attempt -lt 30; $attempt++) {
        Start-Sleep -Milliseconds 150
        if (Test-GraphicCardSitePort) {
            $ready = $true
            break
        }
    }

    if (-not $ready) {
        throw "The graphics-card site server did not start. Check .graphiccardsite-server.log"
    }
}

if (-not $NoBrowser) {
    Start-Process $Url
}

Write-Output $Url
