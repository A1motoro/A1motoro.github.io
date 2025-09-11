@echo off
echo ========================================
echo    MOVING CODING FILES TO CODE FOLDER
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "index.html" (
    echo ERROR: Please run this from the AIE folder
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo Creating code directory structure...
if not exist "code" mkdir code
if not exist "code\python" mkdir code\python
if not exist "code\cpp" mkdir code\cpp
if not exist "code\data" mkdir code\data
if not exist "code\executables" mkdir code\executables

echo.
echo Moving Python files...
if exist "ana.py" (
    move ana.py code\python\
    echo Moved: ana.py -> code\python\
)
if exist "anls.py" (
    move anls.py code\python\
    echo Moved: anls.py -> code\python\
)
if exist "test.py" (
    move test.py code\python\
    echo Moved: test.py -> code\python\
)
if exist "update_blog.py" (
    move update_blog.py code\python\
    echo Moved: update_blog.py -> code\python\
)

echo.
echo Moving C++ source files...
if exist "linkeasy.cpp" (
    move linkeasy.cpp code\cpp\
    echo Moved: linkeasy.cpp -> code\cpp\
)
if exist "linked.cpp" (
    move linked.cpp code\cpp\
    echo Moved: linked.cpp -> code\cpp\
)
if exist "tst.cpp" (
    move tst.cpp code\cpp\
    echo Moved: tst.cpp -> code\cpp\
)
if exist "tst_fast.cpp" (
    move tst_fast.cpp code\cpp\
    echo Moved: tst_fast.cpp -> code\cpp\
)

echo.
echo Moving executables...
if exist "linkeasy.exe" (
    move linkeasy.exe code\executables\
    echo Moved: linkeasy.exe -> code\executables\
)
if exist "linked.exe" (
    move linked.exe code\executables\
    echo Moved: linked.exe -> code\executables\
)
if exist "tst.exe" (
    move tst.exe code\executables\
    echo Moved: tst.exe -> code\executables\
)
if exist "tst_fast.exe" (
    move tst_fast.exe code\executables\
    echo Moved: tst_fast.exe -> code\executables\
)
if exist "CursorUserSetup-x64-1.5.9.exe" (
    move CursorUserSetup-x64-1.5.9.exe code\executables\
    echo Moved: CursorUserSetup-x64-1.5.9.exe -> code\executables\
)

echo.
echo Moving data files...
if exist "UM_C19_2021.csv" (
    move UM_C19_2021.csv code\data\
    echo Moved: UM_C19_2021.csv -> code\data\
)

echo.
echo Moving other files...
if exist "wbtest.html" (
    move wbtest.html code\
    echo Moved: wbtest.html -> code\
)
if exist "requirements.txt" (
    move requirements.txt code\python\
    echo Moved: requirements.txt -> code\python\
)

echo.
echo Removing duplicate folders...
if exist "posts" (
    rmdir /s /q posts
    echo Removed: posts (duplicate)
)
if exist "templates" (
    rmdir /s /q templates
    echo Removed: templates (duplicate)
)
if exist "css" (
    rmdir /s /q css
    echo Removed: css (duplicate)
)
if exist "csv-analyzer.html" (
    del csv-analyzer.html
    echo Removed: csv-analyzer.html (duplicate)
)

echo.
echo Removing Python cache...
if exist "__pycache__" (
    rmdir /s /q __pycache__
    echo Removed: __pycache__
)

echo.
echo Removing other files...
if exist "output" (
    rmdir /s /q output
    echo Removed: output
)
if exist "gitignore.txt" (
    del gitignore.txt
    echo Removed: gitignore.txt
)
if exist "Screenshot_cursorPro.png" (
    move Screenshot_cursorPro.png code\
    echo Moved: Screenshot_cursorPro.png -> code\
)

echo.
echo ========================================
echo    CODING FILES ORGANIZATION COMPLETE!
echo ========================================
echo.
echo All coding files have been moved to the code/ folder:
echo - Python files -> code/python/
echo - C++ files -> code/cpp/
echo - Executables -> code/executables/
echo - Data files -> code/data/
echo - Other files -> code/
echo.
echo Duplicate folders and files have been removed.
echo Your main directory is now clean for website management!
echo.
pause
