@echo off
echo ========================================
echo    AIE PORTFOLIO - UPDATE TOOL
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "index.html" (
    echo ERROR: Please run this from the AIE folder
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo Launching Master Update Tool...
echo.
cd scripts
call master_update.bat
cd ..
