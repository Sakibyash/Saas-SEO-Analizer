@echo off
set "PROJECT_ROOT=%~dp0"
set "NODE_ROOT=%PROJECT_ROOT%nodejs"
set "PATH=%NODE_ROOT%;%NODE_ROOT%\node_modules\.bin;%PATH%"

echo Installing Yarn globally...
call "%NODE_ROOT%\npm.cmd" install -g yarn

echo Setting up project with Yarn...
call yarn install

echo Setup complete!
pause
