# Organize Code Files Script
# PowerShell version for better reliability

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    ORGANIZING CODE FILES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Create directory structure
Write-Host "Creating code directory structure..." -ForegroundColor Yellow
$directories = @("code", "code\python", "code\cpp", "code\data", "code\executables")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Created: $dir" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Moving files..." -ForegroundColor Yellow

# Move Python files
$pythonFiles = @("ana.py", "anls.py", "test.py")
foreach ($file in $pythonFiles) {
    if (Test-Path $file) {
        Move-Item $file "code\python\" -Force
        Write-Host "Moved: $file -> code\python\" -ForegroundColor Green
    }
}

# Move C++ source files
$cppFiles = @("linkeasy.cpp", "linked.cpp", "tst.cpp", "tst_fast.cpp")
foreach ($file in $cppFiles) {
    if (Test-Path $file) {
        Move-Item $file "code\cpp\" -Force
        Write-Host "Moved: $file -> code\cpp\" -ForegroundColor Green
    }
}

# Move executables
$exeFiles = @("linkeasy.exe", "linked.exe", "tst.exe", "tst_fast.exe")
foreach ($file in $exeFiles) {
    if (Test-Path $file) {
        Move-Item $file "code\executables\" -Force
        Write-Host "Moved: $file -> code\executables\" -ForegroundColor Green
    }
}

# Move data files
if (Test-Path "UM_C19_2021.csv") {
    Move-Item "UM_C19_2021.csv" "code\data\" -Force
    Write-Host "Moved: UM_C19_2021.csv -> code\data\" -ForegroundColor Green
}

# Move other code files
if (Test-Path "wbtest.html") {
    Move-Item "wbtest.html" "code\" -Force
    Write-Host "Moved: wbtest.html -> code\" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    ORGANIZATION COMPLETE!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Files have been organized into:" -ForegroundColor White
Write-Host "- code\python\     (Python scripts)" -ForegroundColor Gray
Write-Host "- code\cpp\        (C++ source files)" -ForegroundColor Gray
Write-Host "- code\executables\ (Compiled executables)" -ForegroundColor Gray
Write-Host "- code\data\       (Data files)" -ForegroundColor Gray
Write-Host "- code\            (Other code files)" -ForegroundColor Gray
Write-Host ""
Write-Host "Press Enter to continue..." -ForegroundColor Yellow
Read-Host
