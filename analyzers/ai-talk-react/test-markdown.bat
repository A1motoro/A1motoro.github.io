@echo off
echo ===============================================
echo    TESTING MARKDOWN FEATURES
echo ===============================================
echo.

cd /d "%~dp0"

echo Checking if markdown dependencies are installed...
node -e "try { require('react-markdown'); console.log('✅ react-markdown: OK'); } catch(e) { console.log('❌ react-markdown: MISSING - Run install-markdown.bat'); }"
node -e "try { require('react-syntax-highlighter'); console.log('✅ react-syntax-highlighter: OK'); } catch(e) { console.log('❌ react-syntax-highlighter: MISSING - Run install-markdown.bat'); }"
node -e "try { require('remark-gfm'); console.log('✅ remark-gfm: OK'); } catch(e) { console.log('❌ remark-gfm: MISSING - Run install-markdown.bat'); }"

echo.
echo If all dependencies are OK, start the app with:
echo start-local.bat
echo.
echo Then test markdown by asking Qwen:
echo "Write a Python function with syntax highlighting"
echo.
pause
