@echo off
echo ========================================
<<<<<<< HEAD
echo    AIE PORTFOLIO - ONE CLICK UPDATE
=======
echo    BLOGIIIIII - ONE CLICK UPDATE
>>>>>>> 0e92592fdaf42209d9a2b86a17eb2a04dd8613f8
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "index.html" (
<<<<<<< HEAD
    echo ERROR: Please run this from the AIE folder
=======
    echo ERROR: Please run this from the blogii folder
>>>>>>> 0e92592fdaf42209d9a2b86a17eb2a04dd8613f8
    echo Current directory: %CD%
    pause
    exit /b 1
)

<<<<<<< HEAD
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
=======
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
>>>>>>> 0e92592fdaf42209d9a2b86a17eb2a04dd8613f8
"C:\Program Files\Git\bin\git.exe" add .
if errorlevel 1 (
    echo ERROR: Failed to add files to Git
    pause
    exit /b 1
)

echo.
<<<<<<< HEAD
echo [3/4] Committing changes...
"C:\Program Files\Git\bin\git.exe" commit -m "Update portfolio - %date% %time%"
=======
echo [3/3] Committing and pushing to GitHub...
"C:\Program Files\Git\bin\git.exe" commit -m "Update blog - %date% %time%"
>>>>>>> 0e92592fdaf42209d9a2b86a17eb2a04dd8613f8
if errorlevel 1 (
    echo WARNING: Nothing to commit (no changes detected)
) else (
    echo Changes committed successfully
)

<<<<<<< HEAD
echo.
echo [4/4] Pushing to GitHub...
=======
>>>>>>> 0e92592fdaf42209d9a2b86a17eb2a04dd8613f8
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
<<<<<<< HEAD
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
=======
echo Your blog has been updated and uploaded to GitHub!
echo It will be live at: https://A1motoro.github.io
echo.
echo Changes should be visible in 2-5 minutes.
echo.
echo Closing in 3 seconds...
timeout /t 3 /nobreak >nul
>>>>>>> 0e92592fdaf42209d9a2b86a17eb2a04dd8613f8
exit /b 0
