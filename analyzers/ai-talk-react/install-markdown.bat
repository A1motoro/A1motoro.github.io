@echo off
echo ===============================================
echo    INSTALLING MARKDOWN DEPENDENCIES
echo ===============================================
echo.

cd /d "%~dp0"

echo Installing markdown rendering libraries...
echo This will add react-markdown, react-syntax-highlighter, and remark-gfm
echo.

npm install react-markdown react-syntax-highlighter remark-gfm

echo.
echo ===============================================
echo         MARKDOWN FEATURES INSTALLED!
echo ===============================================
echo.
echo Your AI Talk app now supports:
echo ✅ Full markdown rendering
echo ✅ Syntax highlighted code blocks (Monokai theme)
echo ✅ GitHub Flavored Markdown
echo.
echo Restart your development server to see the changes!
echo.
pause
