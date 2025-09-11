# AIE Portfolio - One Click Update Script
# PowerShell version for better compatibility

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    AIE PORTFOLIO - ONE CLICK UPDATE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "index.html")) {
    Write-Host "ERROR: Please run this from the AIE folder" -ForegroundColor Red
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Starting portfolio update..." -ForegroundColor Green
Write-Host ""

# Step 1: Update blog content (if needed)
Write-Host "[1/4] Checking blog updates..." -ForegroundColor Yellow
if (Test-Path "blogii\update_blog.py") {
    Set-Location "blogii"
    try {
        python update_blog.py
        Write-Host "Blog update completed" -ForegroundColor Green
    } catch {
        Write-Host "WARNING: Blog update failed, continuing..." -ForegroundColor Yellow
    }
    Set-Location ".."
} else {
    Write-Host "No blog update script found, skipping..." -ForegroundColor Gray
}

Write-Host ""
Write-Host "[2/4] Adding all files to Git..." -ForegroundColor Yellow
try {
    git add .
    Write-Host "Files added successfully" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to add files to Git" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[3/4] Committing changes..." -ForegroundColor Yellow
$commitMessage = "Update portfolio - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
try {
    git commit -m $commitMessage
    Write-Host "Changes committed successfully" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Nothing to commit (no changes detected)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[4/4] Pushing to GitHub..." -ForegroundColor Yellow
try {
    git push origin main
    Write-Host "Push completed successfully" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to push to GitHub" -ForegroundColor Red
    Write-Host "Please check your internet connection and GitHub repository settings" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    UPDATE COMPLETE!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your portfolio has been updated and uploaded to GitHub!" -ForegroundColor Green
Write-Host "It will be live at: https://a1motoro.github.io" -ForegroundColor Cyan
Write-Host ""
Write-Host "Changes should be visible in 2-5 minutes." -ForegroundColor Yellow
Write-Host ""
Write-Host "Portfolio includes:" -ForegroundColor White
Write-Host "- Main landing page (index.html)" -ForegroundColor Gray
Write-Host "- Blog section (blogii/)" -ForegroundColor Gray
Write-Host "- Data analysis tools (data-analysis/)" -ForegroundColor Gray
Write-Host "- Core framework (core-framework/)" -ForegroundColor Gray
Write-Host ""
Write-Host "Closing in 5 seconds..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
exit 0
