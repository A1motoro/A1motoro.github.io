@echo off
echo 🌳 Setting up Git Branch Strategy for AIE Portfolio...
echo.

REM Check if we're in a git repository
if not exist ".git" (
    echo ❌ Error: Not in a git repository!
    echo Please initialize git first: git init
    pause
    exit /b 1
)

echo 📋 Current git status:
git status
echo.

echo 💾 Stashing any uncommitted changes...
git stash push -m "Setup branch strategy - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
echo.

echo 🌿 Creating branch structure...
echo.

REM Create blog branch
echo 📝 Creating blog branch...
git checkout -b blog
if exist "blogii" (
    echo Moving blog content to blog branch root...
    xcopy "blogii\*" "." /E /I /Y
    rmdir /s /q "blogii"
)
git add .
git commit -m "feat: initialize blog branch with blog content"
echo ✅ Blog branch created
echo.

REM Create analyzers branch
echo 📊 Creating analyzers branch...
git checkout main
git checkout -b analyzers
if exist "analyzers" (
    echo Moving analyzers content to analyzers branch root...
    xcopy "analyzers\*" "." /E /I /Y
    rmdir /s /q "analyzers"
)
git add .
git commit -m "feat: initialize analyzers branch with analysis tools"
echo ✅ Analyzers branch created
echo.

REM Create development branch
echo 🛠️ Creating development branch...
git checkout main
git checkout -b development
if exist "code" (
    echo Moving development content to development branch root...
    xcopy "code\*" "." /E /I /Y
    rmdir /s /q "code"
)
git add .
git commit -m "feat: initialize development branch with source code"
echo ✅ Development branch created
echo.

REM Create docs branch
echo 📚 Creating docs branch...
git checkout main
git checkout -b docs
if exist "docs" (
    echo Moving documentation to docs branch root...
    xcopy "docs\*" "." /E /I /Y
    rmdir /s /q "docs"
)
git add .
git commit -m "feat: initialize docs branch with documentation"
echo ✅ Docs branch created
echo.

REM Clean up main branch
echo 🧹 Cleaning up main branch...
git checkout main

REM Remove content that belongs to other branches
echo Removing content that belongs to other branches...
if exist "blogii" rmdir /s /q "blogii"
if exist "analyzers" rmdir /s /q "analyzers"
if exist "code" rmdir /s /q "code"
if exist "docs" rmdir /s /q "docs"
if exist "portfolio-js.html" del "portfolio-js.html"
if exist "index-js.html" del "index-js.html"

REM Keep only core framework, portfolio, and essential files
echo Keeping only core framework and portfolio content...
git add .
git commit -m "feat: clean up main branch - keep only core framework and portfolio"
echo ✅ Main branch cleaned up
echo.

REM Push all branches to remote
echo 📤 Pushing all branches to remote...
git push -u origin main
git push -u origin blog
git push -u origin analyzers
git push -u origin development
git push -u origin docs
echo ✅ All branches pushed to remote
echo.

REM Restore stashed changes
echo 🔄 Restoring stashed changes...
git stash pop
echo.

echo 🎉 Branch strategy setup completed!
echo.
echo 📋 Summary of branches created:
echo   • main: Core framework, portfolio, public content
echo   • blog: Blog content and management tools
echo   • analyzers: Data analysis tools
echo   • development: Source code and development tools
echo   • docs: Documentation and guides
echo.
echo 🔐 Next steps:
echo   1. Configure branch protection rules on GitHub
echo   2. Set up access controls for each branch
echo   3. Configure GitHub Pages for each branch
echo   4. Create deployment scripts for each branch
echo.
echo 📖 See BRANCH_STRATEGY.md for detailed workflow information
echo.
pause
