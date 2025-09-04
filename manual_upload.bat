@echo off
echo ========================================
echo    BLOGIIIIII - Manual Upload Helper
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "index.html" (
    echo ERROR: Please run this from the blogii folder
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo This will help you upload your blog manually to GitHub.
echo.

echo [1/2] Updating blog content...
python update_blog.py
if errorlevel 1 (
    echo ERROR: Failed to update blog content
    pause
    exit /b 1
)

echo.
echo [2/2] Preparing files for upload...
echo.
echo Files ready for upload:
dir /b

echo.
echo ========================================
echo    Manual Upload Instructions
echo ========================================
echo.
echo 1. Go to your GitHub repository:
echo    https://github.com/A1motoro/A1motoro.github.io
echo.
echo 2. Click "Add file" - "Upload files"
echo.
echo 3. Drag and drop ALL files from this folder:
echo    %CD%
echo.
echo 4. Add commit message: "Update BLOGIIIIII"
echo.
echo 5. Click "Commit changes"
echo.
echo Your blog will be live at:
echo https://A1motoro.github.io
echo.
echo Changes will be visible in 2-5 minutes!
echo.
pause