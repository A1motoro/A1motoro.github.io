# Fix Git Push Issue Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    FIXING GIT PUSH ISSUE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/3] Pulling remote changes..." -ForegroundColor Yellow
try {
    git pull origin main --allow-unrelated-histories
    Write-Host "Pull completed successfully" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Pull failed, trying rebase..." -ForegroundColor Yellow
    try {
        git pull origin main --rebase
        Write-Host "Rebase pull completed" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Both pull methods failed" -ForegroundColor Red
        Write-Host "You may need to resolve conflicts manually" -ForegroundColor Red
        Read-Host "Press Enter to continue anyway"
    }
}

Write-Host ""
Write-Host "[2/3] Adding local changes..." -ForegroundColor Yellow
git add .
Write-Host "Files added successfully" -ForegroundColor Green

Write-Host ""
Write-Host "[3/3] Committing and pushing..." -ForegroundColor Yellow
try {
    git commit -m "Update main page, hide code section, and reorganize navigation"
    Write-Host "Commit successful" -ForegroundColor Green
    
    git push origin main
    Write-Host "Push successful" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Commit or push failed" -ForegroundColor Red
    Write-Host "Please check your Git configuration" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    UPDATE COMPLETE!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your changes have been successfully pushed to GitHub!" -ForegroundColor Green
Write-Host "Website will be live at: https://a1motoro.github.io" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Enter to continue..." -ForegroundColor Yellow
Read-Host
