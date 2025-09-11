@echo off
echo ========================================
echo    FIXING GITHUB PAGES DEPLOYMENT
echo ========================================
echo.

REM Force navigation to D:\AIE
cd /d "D:\AIE"

echo [1/5] Checking current status...
git status

echo.
echo [2/5] Removing any submodule references...
git rm --cached blogii 2>nul
git add blogii/

echo.
echo [3/5] Committing changes...
git commit -m "Force remove submodule references, add blogii as regular folder"

echo.
echo [4/5] Force pushing to main branch...
git push origin main --force

echo.
echo [5/5] Checking final status...
git status

echo.
echo ========================================
echo    GITHUB PAGES FIX COMPLETE!
echo ========================================
echo.
echo The submodule issue should now be resolved.
echo GitHub Pages will rebuild automatically.
echo.
pause
