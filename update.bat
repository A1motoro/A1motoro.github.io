@echo off
echo ========================================
echo    AIE PORTFOLIO - UPDATE TOOL
echo ========================================
echo.

REM Force navigation to D:\AIE (where we know the project is)
echo Navigating to D:\AIE...
cd /d "D:\AIE"

REM Verify we're in the right place
if not exist "index.html" (
    echo ERROR: index.html not found in D:\AIE
    echo Please check if the AIE folder exists at D:\AIE
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo Found AIE folder at: %CD%
echo Launching Master Update Tool...
echo.
cd scripts
call master_update.bat
cd ..
