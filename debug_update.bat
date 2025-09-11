@echo off
echo ========================================
echo    DEBUG UPDATE SCRIPT
echo ========================================
echo.

echo Current directory: %CD%
echo Script location: %~dp0
echo.

echo Checking for index.html in various locations:
echo.

REM Check current directory
if exist "index.html" (
    echo [FOUND] Current directory: %CD%\index.html
    set AIE_FOLDER=%CD%
    goto :found
) else (
    echo [NOT FOUND] Current directory: %CD%\index.html
)

REM Check parent directory
if exist "..\index.html" (
    echo [FOUND] Parent directory: %CD%\..\index.html
    set AIE_FOLDER=%CD%\..
    goto :found
) else (
    echo [NOT FOUND] Parent directory: %CD%\..\index.html
)

REM Check grandparent directory
if exist "..\..\index.html" (
    echo [FOUND] Grandparent directory: %CD%\..\..\index.html
    set AIE_FOLDER=%CD%\..\..
    goto :found
) else (
    echo [NOT FOUND] Grandparent directory: %CD%\..\..\index.html
)

REM Check D:\AIE
if exist "D:\AIE\index.html" (
    echo [FOUND] D:\AIE\index.html
    set AIE_FOLDER=D:\AIE
    goto :found
) else (
    echo [NOT FOUND] D:\AIE\index.html
)

echo.
echo ERROR: Could not find index.html in any location
echo Please check if index.html exists in the AIE folder
pause
exit /b 1

:found
echo.
echo SUCCESS: Found AIE folder at: %AIE_FOLDER%
echo Navigating to: %AIE_FOLDER%
cd /d "%AIE_FOLDER%"
echo Current directory after navigation: %CD%

echo.
echo Launching Master Update Tool...
cd scripts
call master_update.bat
cd ..
