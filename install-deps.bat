@echo off
set "PROJECT_ROOT=%~dp0"
set "NODE_ROOT=%PROJECT_ROOT%nodejs"
set "PATH=%NODE_ROOT%;%NODE_ROOT%\node_modules\.bin;%PATH%"
set "NODE_PATH=%NODE_ROOT%\node_modules"
set "NPM_CONFIG_PREFIX=%NODE_ROOT%"

echo Installing Next.js and React...
call "%NODE_ROOT%\npm.cmd" install next@14.0.4 react@18.2.0 react-dom@18.2.0

echo Installing TypeScript dependencies...
call "%NODE_ROOT%\npm.cmd" install typescript@5.3.3 @types/node@20.10.5 @types/react@18.2.45 @types/react-dom@18.2.18

echo Installing styling dependencies...
call "%NODE_ROOT%\npm.cmd" install autoprefixer@10.4.16 postcss@8.4.32 tailwindcss@3.4.0

echo Installing ESLint...
call "%NODE_ROOT%\npm.cmd" install eslint@8.56.0 eslint-config-next@14.0.4

echo Dependencies installation complete!
pause
