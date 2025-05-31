@echo off
set "PROJECT_ROOT=%~dp0"
set "NODE_ROOT=%PROJECT_ROOT%nodejs"
set "PATH=%NODE_ROOT%;%NODE_ROOT%\node_modules\.bin;%PATH%"
set "NODE_PATH=%NODE_ROOT%\node_modules"
set "NPM_CONFIG_PREFIX=%NODE_ROOT%"

echo Installing create-next-app globally...
call "%NODE_ROOT%\npm" install -g create-next-app

echo Creating Next.js project...
call create-next-app . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --no-git

echo Setup complete!
pause
