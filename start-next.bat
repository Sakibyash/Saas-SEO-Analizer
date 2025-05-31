@echo off
echo Setting up portable Node.js environment...
set "PROJECT_ROOT=%~dp0"
set "NODE_ROOT=%PROJECT_ROOT%nodejs"
set "PATH=%NODE_ROOT%;%NODE_ROOT%\node_modules\.bin;%PATH%"
set "NODE_PATH=%NODE_ROOT%\node_modules"
set "NPM_CONFIG_PREFIX=%NODE_ROOT%"

echo Checking Node.js installation...
node --version
if errorlevel 1 (
    echo Error: Node.js not found in nodejs directory
    pause
    exit /b 1
)

echo Checking npm installation...
call npm --version
if errorlevel 1 (
    echo Error: npm not found in nodejs directory
    pause
    exit /b 1
)

echo Checking npx availability...
call npx --version
if errorlevel 1 (
    echo Error: npx not found in nodejs directory
    pause
    exit /b 1
)

echo === Development Environment Ready ===
echo Node version: 
node --version
echo npm version:
call npm --version
echo npx version:
call npx --version

echo Starting development shell...
cmd /k "echo Ready to create Next.js project"
