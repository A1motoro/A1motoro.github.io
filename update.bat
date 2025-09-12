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
echo.
echo Choose update method:
echo 1. Deploy specific branch
echo 2. Deploy all branches
echo 3. Setup branch strategy (first time)
echo 4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Launching branch deployment tool...
    call deploy_branch.bat
) else if "%choice%"=="2" (
    echo.
    echo Deploying all branches...
    git add .
    git commit -m "update: sync all changes - %date% %time%"
    git push origin main
    git push origin blog
    git push origin analyzers
    git push origin development
    git push origin docs
    echo.
    echo ✅ All branches updated successfully!
) else if "%choice%"=="3" (
    echo.
    echo Setting up branch strategy...
    call setup_branch_strategy.bat
) else if "%choice%"=="4" (
    echo.
    echo Goodbye!
    exit /b 0
) else (
    echo.
    echo ❌ Invalid choice. Please try again.
    pause
    goto :eof
)

echo.
echo 🎉 Update completed!
pause