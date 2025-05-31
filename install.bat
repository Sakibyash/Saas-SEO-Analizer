@echo off
set "PROJECT_ROOT=%~dp0"
set "NODE_ROOT=%PROJECT_ROOT%nodejs"
set "PATH=%NODE_ROOT%;%NODE_ROOT%\node_modules\.bin;%PATH%"
set "NODE_PATH=%NODE_ROOT%\node_modules"
set "NPM_CONFIG_PREFIX=%NODE_ROOT%"

echo Installing dependencies...
call "%NODE_ROOT%\npm.cmd" install

echo Installation complete!
pause
