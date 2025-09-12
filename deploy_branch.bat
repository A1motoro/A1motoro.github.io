@echo off
echo 🚀 AIE Portfolio - Branch Deployment System
echo.

echo 📋 Available branches for deployment:
echo   1. main (Portfolio & Core Framework)
echo   2. blog (Blog Content)
echo   3. analyzers (Data Analysis Tools)
echo   4. development (Source Code)
echo   5. docs (Documentation)
echo   6. Deploy All Branches
echo   7. Exit
echo.

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" (
    echo 🏠 Deploying main branch...
    git checkout main
    git pull origin main
    git add .
    git commit -m "deploy: update main branch - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git push origin main
    echo ✅ Main branch deployed successfully!
    echo 📍 Public portfolio and core framework updated
) else if "%choice%"=="2" (
    echo 📝 Deploying blog branch...
    git checkout blog
    git pull origin blog
    git add .
    git commit -m "deploy: update blog content - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git push origin blog
    echo ✅ Blog branch deployed successfully!
    echo 📍 Blog content updated (limited access)
) else if "%choice%"=="3" (
    echo 📊 Deploying analyzers branch...
    git checkout analyzers
    git pull origin analyzers
    git add .
    git commit -m "deploy: update analyzers - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git push origin analyzers
    echo ✅ Analyzers branch deployed successfully!
    echo 📍 Data analysis tools updated (private access)
) else if "%choice%"=="4" (
    echo 🛠️ Deploying development branch...
    git checkout development
    git pull origin development
    git add .
    git commit -m "deploy: update development code - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git push origin development
    echo ✅ Development branch deployed successfully!
    echo 📍 Source code updated (private access)
) else if "%choice%"=="5" (
    echo 📚 Deploying docs branch...
    git checkout docs
    git pull origin docs
    git add .
    git commit -m "deploy: update documentation - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git push origin docs
    echo ✅ Docs branch deployed successfully!
    echo 📍 Documentation updated (public access)
) else if "%choice%"=="6" (
    echo 🚀 Deploying all branches...
    echo.
    echo Deploying main branch...
    git checkout main
    git pull origin main
    git add .
    git commit -m "deploy: update main branch - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git push origin main
    echo.
    echo Deploying blog branch...
    git checkout blog
    git pull origin blog
    git add .
    git commit -m "deploy: update blog content - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git push origin blog
    echo.
    echo Deploying analyzers branch...
    git checkout analyzers
    git pull origin analyzers
    git add .
    git commit -m "deploy: update analyzers - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git push origin analyzers
    echo.
    echo Deploying development branch...
    git checkout development
    git pull origin development
    git add .
    git commit -m "deploy: update development code - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git push origin development
    echo.
    echo Deploying docs branch...
    git checkout docs
    git pull origin docs
    git add .
    git commit -m "deploy: update documentation - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git push origin docs
    echo.
    echo ✅ All branches deployed successfully!
) else if "%choice%"=="7" (
    echo 👋 Goodbye!
    exit /b 0
) else (
    echo ❌ Invalid choice. Please try again.
    pause
    goto :eof
)

echo.
echo 🎉 Deployment completed!
echo.
echo 📖 For detailed workflow information, see BRANCH_STRATEGY.md
echo.
pause
