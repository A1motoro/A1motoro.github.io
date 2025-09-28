# AI Talk React Local Development Launcher
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   STARTING AI TALK REACT LOCALLY" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Get the directory where this script is located
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "Starting AI Talk React development server..." -ForegroundColor Green
Write-Host "This will open http://localhost:3000 in your browser" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the development server
npm start
