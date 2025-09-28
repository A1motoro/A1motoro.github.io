@echo off
echo ===============================================
echo    INSTALLING DATA ANALYZER DEPENDENCIES
echo ===============================================
echo.

cd /d "%~dp0"

echo Installing all required packages for the Data Analyzer...
echo This includes React, Chart.js, PapaParse, and AI dependencies
echo.

npm install

echo.
echo ===============================================
echo         DEPENDENCIES INSTALLED!
echo ===============================================
echo.
echo Your Data Analyzer is now ready with:
echo ✅ React and TypeScript
echo ✅ Chart.js for visualizations
echo ✅ PapaParse for CSV processing
echo ✅ AI insights with markdown support
echo.
echo To start the analyzer, run:
echo start-analyzer.bat
echo.
pause
