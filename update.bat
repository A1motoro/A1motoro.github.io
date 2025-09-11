@echo off
echo ========================================
echo    AIE PORTFOLIO - UPDATE TOOL
echo ========================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
echo Script location: %SCRIPT_DIR%

REM Navigate to the script directory (AIE folder)
cd /d "%SCRIPT_DIR%"

REM Check if we're in the right directory
if not exist "index.html" (
    echo ERROR: index.html not found in %SCRIPT_DIR%
    echo Please ensure this script is in the AIE folder
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo Found index.html - launching Master Update Tool...
echo.
cd scripts
call master_update.bat
cd ..
