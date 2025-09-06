@echo off
echo ========================================
echo    BLOGIIIIII - ONE CLICK UPDATE
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "index.html" (
    echo ERROR: Please run this from the blogii folder
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo Starting blog update...
echo.

REM Step 1: Update blog content
echo [1/3] Updating blog content...
python update_blog.py
if errorlevel 1 (
    echo ERROR: Failed to update blog content
    pause
    exit /b 1
)

echo.
echo [2/3] Adding files to Git...
"C:\Program Files\Git\bin\git.exe" add .
if errorlevel 1 (
    echo ERROR: Failed to add files to Git
    pause
    exit /b 1
)

echo.
echo [3/3] Committing and pushing to GitHub...
"C:\Program Files\Git\bin\git.exe" commit -m "Update blog - %date% %time%"
if errorlevel 1 (
    echo WARNING: Nothing to commit (no changes detected)
) else (
    echo Changes committed successfully
)

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
echo Your blog has been updated and uploaded to GitHub!
echo It will be live at: https://A1motoro.github.io
echo.
echo Changes should be visible in 2-5 minutes.
echo.
echo Closing in 3 seconds...
timeout /t 3 /nobreak >nul
exit /b 0
