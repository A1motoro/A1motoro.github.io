@echo off
echo Updating repository...
git add .
git commit -m "Update main page, hide code section, and reorganize navigation"
git push origin main
echo Update complete!
pause
