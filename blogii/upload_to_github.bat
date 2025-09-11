@echo off
echo Uploading BLOGIIIIII to GitHub...

REM Add all files
git add .

REM Commit changes
git commit -m "Update blog posts - %date% %time%"

REM Push to GitHub
git push origin main

echo Blog updated successfully!
pause
