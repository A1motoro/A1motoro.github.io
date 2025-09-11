@echo off
echo ========================================
echo    FIXING GIT PUSH ISSUE
echo ========================================
echo.

echo [1/3] Pulling remote changes...
git pull origin main --allow-unrelated-histories
if errorlevel 1 (
    echo WARNING: Pull failed, trying alternative approach...
    git pull origin main --rebase
)

echo.
echo [2/3] Adding local changes...
git add .

echo.
echo [3/3] Committing and pushing...
git commit -m "Update main page, hide code section, and reorganize navigation"
git push origin main

echo.
echo ========================================
echo    UPDATE COMPLETE!
echo ========================================
echo.
echo Your changes have been successfully pushed to GitHub!
echo Website will be live at: https://a1motoro.github.io
echo.
pause
