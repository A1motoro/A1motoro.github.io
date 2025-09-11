@echo off
echo ========================================
echo    AIE PORTFOLIO - UPDATE TOOL (ANYWHERE)
echo ========================================
echo.

REM Try to find the AIE folder
set AIE_FOLDER=

REM Check current directory first
if exist "index.html" (
    set AIE_FOLDER=%CD%
    goto :found
)

REM Check parent directory
cd ..
if exist "index.html" (
    set AIE_FOLDER=%CD%
    goto :found
)

REM Check if we're in a subdirectory of AIE
cd /d "%~dp0"
if exist "index.html" (
    set AIE_FOLDER=%CD%
    goto :found
)

REM Look for AIE folder in common locations
if exist "D:\AIE\index.html" (
    set AIE_FOLDER=D:\AIE
    goto :found
)

if exist "C:\AIE\index.html" (
    set AIE_FOLDER=C:\AIE
    goto :found
)

echo ERROR: Could not find AIE folder with index.html
echo Please run this from the AIE folder or ensure AIE is in D:\ or C:\
echo Current directory: %CD%
pause
exit /b 1

:found
echo Found AIE folder: %AIE_FOLDER%
cd /d "%AIE_FOLDER%"

echo Launching Master Update Tool...
echo.
cd scripts
call master_update.bat
cd ..
