@echo off
echo ===============================================
echo    QUICK FIX FOR REACT TYPESCRIPT ERRORS
echo ===============================================
echo.

cd /d "%~dp0"

echo Step 1: Checking Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found!
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)
echo Node.js OK
echo.

echo Step 2: Installing only essential packages...
call ..\..\nodejs\node-v18.19.0-win-x64\npm.cmd install react react-dom typescript @types/react @types/react-dom --save
if %errorlevel% neq 0 (
    echo ERROR: Installation failed!
    pause
    exit /b 1
)
echo Essential packages installed
echo.

echo Step 3: Testing React import...
call ..\..\nodejs\node-v18.19.0-win-x64\node.exe -e "try { require('react'); console.log('React: OK'); } catch(e) { console.log('React: FAILED -', e.message); }"
echo.

echo ===============================================
echo         REACT ERRORS SHOULD BE FIXED!
echo ===============================================
echo.
echo Try opening your React app now.
echo.
echo If you still see errors, use:
echo working-app.html (works without npm)
echo.
pause
