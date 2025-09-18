@echo off
echo ===============================================
echo       AI Talk Troubleshooting Script
echo ===============================================
echo.

echo Checking Node.js installation...
node --version
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed!
    echo Please download and install Node.js from:
    echo https://nodejs.org/en/download/
    echo.
    pause
    exit /b 1
)
echo Node.js is installed ✓
echo.

echo Checking npm installation...
npm --version
if %errorlevel% neq 0 (
    echo ERROR: npm is not working!
    echo npm should come with Node.js installation
    echo.
    pause
    exit /b 1
)
echo npm is installed ✓
echo.

echo Checking current directory...
cd /d "%~dp0"
echo Current directory: %CD%
echo.

echo Checking for package.json...
if not exist package.json (
    echo ERROR: package.json not found!
    echo This doesn't seem to be a Node.js project
    pause
    exit /b 1
)
echo package.json found ✓
echo.

echo Checking node_modules...
if not exist node_modules (
    echo node_modules not found - will install dependencies
    set INSTALL_NEEDED=1
) else (
    echo node_modules exists ✓
    if not exist node_modules\react (
        echo WARNING: React not found in node_modules
        set INSTALL_NEEDED=1
    )
    if not exist node_modules\typescript (
        echo WARNING: TypeScript not found in node_modules
        set INSTALL_NEEDED=1
    )
)
echo.

echo Checking npm cache...
npm cache verify
echo.

if defined INSTALL_NEEDED (
    echo Installing dependencies...
    echo This may take a few minutes...
    npm install --no-optional
    if %errorlevel% neq 0 (
        echo ERROR: Installation failed!
        echo Try running: npm cache clean --force
        echo Then run this script again
        pause
        exit /b 1
    )
    echo Installation completed ✓
    echo.
)

echo Testing React import...
node -e "try { require('react'); console.log('React import: ✓'); } catch(e) { console.log('React import: ✗ -', e.message); }"
echo.

echo Testing TypeScript...
node -e "try { require('typescript'); console.log('TypeScript import: ✓'); } catch(e) { console.log('TypeScript import: ✗ -', e.message); }"
echo.

echo ===============================================
echo         Troubleshooting Complete
echo ===============================================
echo.
echo If you see any ✗ marks above, there may be issues.
echo.
echo To start the development server, run:
echo quick-start.bat
echo.
echo Or manually run:
echo npm start
echo.
pause


