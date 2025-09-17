@echo off
echo Starting AI Talk React Development Server...
echo.

REM Navigate to the correct Node.js directory
set NODE_PATH=..\..\nodejs\node-v18.19.0-win-x64

REM Install dependencies if needed
echo Installing dependencies...
"%NODE_PATH%\npm.cmd" install

REM Start the development server
echo.
echo Starting development server...
"%NODE_PATH%\npm.cmd" start
