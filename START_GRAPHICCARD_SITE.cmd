@echo off
setlocal
cd /d "%~dp0"
"%~dp0.venv\Scripts\python.exe" "%~dp0launch_detached_server.py"
if errorlevel 1 (
  echo.
  echo Failed to start the graphics-card site.
  echo Check: %~dp0.graphiccardsite-server.log
  pause
  exit /b 1
)
start "" "http://localhost:4181/"
endlocal
