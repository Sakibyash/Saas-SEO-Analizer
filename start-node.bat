@echo off
echo Setting up portable Node.js environment...
set "PROJECT_ROOT=%~dp0"
set "NODE_ROOT=%PROJECT_ROOT%nodejs"
set "PATH=%NODE_ROOT%;%NODE_ROOT%\node_modules\.bin;%PATH%"
set "NODE_PATH=%NODE_ROOT%\node_modules"

echo Checking Node.js installation...
node --version
if errorlevel 1 (
    echo Error: Node.js not found in nodejs directory
    echo Please ensure you extracted all contents of node-v20.10.0-win-x64.zip into the nodejs folder
    pause
    exit /b 1
)

echo Checking npm installation...
call npm --version
if errorlevel 1 (
    echo Error: npm not found in nodejs directory
    echo Please ensure npm files are present in the nodejs folder
    pause
    exit /b 1
)

echo Node.js environment ready!
echo Node version: 
node --version
echo npm version:
call npm --version

echo Starting development shell...
cmd /k "echo Environment ready for development"
