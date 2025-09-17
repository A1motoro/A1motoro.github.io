@echo off
echo Building AI Talk React Application...
echo.

REM Navigate to the correct Node.js directory
set NODE_PATH=..\..\nodejs\node-v18.19.0-win-x64

REM Install dependencies if needed
echo Installing dependencies...
"%NODE_PATH%\npm.cmd" install

REM Build the application
echo.
echo Building application...
"%NODE_PATH%\npm.cmd" run build

echo.
echo Build completed! Files are in the 'build' folder.
echo You can now access the application at: analyzers/ai-talk-react/build/index.html
pause
