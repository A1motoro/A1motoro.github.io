@echo off
echo ===============================================
echo    STARTING CSV DATA ANALYZER WITH AI INSIGHTS
echo ===============================================
echo.

cd /d "%~dp0"

echo Installing dependencies if needed...
npm install

echo.
echo Starting the Data Analyzer...
echo This will open http://localhost:3000 in your browser
echo.
echo Features:
echo ✅ Upload and analyze CSV files
echo ✅ Generate beautiful charts
echo ✅ Get AI-powered insights (requires API key)
echo.
echo Press Ctrl+C to stop the server
echo.

npm start

pause
