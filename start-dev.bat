@echo off
echo Setting up portable Node.js environment...
set "PROJECT_ROOT=%~dp0"
set "PATH=%PROJECT_ROOT%nodejs;%PATH%"
set "NODE_PATH=%PROJECT_ROOT%nodejs\node_modules"

echo Checking Node.js installation...
node --version
if errorlevel 1 (
    echo Error: Node.js not found in nodejs directory
    echo Please ensure you extracted all contents of node-v20.10.0-win-x64.zip into the nodejs folder
    pause
    exit /b 1
)

echo Node.js environment ready!
echo Starting development shell...
cmd /k "echo Type 'npm --version' to verify npm installation"
