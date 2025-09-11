@echo off
echo ========================================
echo    AIE PORTFOLIO - ONE CLICK UPDATE
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "index.html" (
    echo ERROR: Please run this from the AIE folder
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo Starting portfolio update...
echo.

REM Step 1: Update blog content (if needed)
echo [1/4] Checking blog updates...
if exist "blogii\update_blog.py" (
    cd blogii
    python update_blog.py
    if errorlevel 1 (
        echo WARNING: Blog update failed, continuing...
    )
    cd ..
) else (
    echo No blog update script found, skipping...
)

echo.
echo [2/4] Adding all files to Git...
"C:\Program Files\Git\bin\git.exe" add .
if errorlevel 1 (
    echo ERROR: Failed to add files to Git
    pause
    exit /b 1
)

echo.
echo [3/4] Committing changes...
"C:\Program Files\Git\bin\git.exe" commit -m "Update portfolio - %date% %time%"
if errorlevel 1 (
    echo WARNING: Nothing to commit (no changes detected)
) else (
    echo Changes committed successfully
)

echo.
echo [4/4] Pushing to GitHub...
"C:\Program Files\Git\bin\git.exe" push origin main
if errorlevel 1 (
    echo ERROR: Failed to push to GitHub
    echo Please check your internet connection and GitHub repository settings
    pause
    exit /b 1
)

echo.
echo ========================================
echo    UPDATE COMPLETE!
echo ========================================
echo.
echo Your portfolio has been updated and uploaded to GitHub!
echo It will be live at: https://a1motoro.github.io
echo.
echo Changes should be visible in 2-5 minutes.
echo.
echo Portfolio includes:
echo - Main landing page (index.html)
echo - Blog section (blogii/)
echo - Data analysis tools (data-analysis/)
echo - Core framework (core-framework/)
echo.
echo Closing in 5 seconds...
timeout /t 5 /nobreak >nul
exit /b 0
