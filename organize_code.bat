@echo off
echo ========================================
echo    ORGANIZING CODE FILES
echo ========================================
echo.

echo Creating code directory structure...
if not exist "code" mkdir code
if not exist "code\python" mkdir code\python
if not exist "code\cpp" mkdir code\cpp
if not exist "code\data" mkdir code\data
if not exist "code\executables" mkdir code\executables

echo.
echo Moving Python files...
if exist "ana.py" move ana.py code\python\
if exist "anls.py" move anls.py code\python\
if exist "test.py" move test.py code\python\

echo Moving C++ source files...
if exist "linkeasy.cpp" move linkeasy.cpp code\cpp\
if exist "linked.cpp" move linked.cpp code\cpp\
if exist "tst.cpp" move tst.cpp code\cpp\
if exist "tst_fast.cpp" move tst_fast.cpp code\cpp\

echo Moving executables...
if exist "linkeasy.exe" move linkeasy.exe code\executables\
if exist "linked.exe" move linked.exe code\executables\
if exist "tst.exe" move tst.exe code\executables\
if exist "tst_fast.exe" move tst_fast.exe code\executables\

echo Moving data files...
if exist "UM_C19_2021.csv" move UM_C19_2021.csv code\data\

echo Moving other files...
if exist "wbtest.html" move wbtest.html code\

echo.
echo ========================================
echo    ORGANIZATION COMPLETE!
echo ========================================
echo.
echo Files have been organized into:
echo - code\python\     (Python scripts)
echo - code\cpp\        (C++ source files)
echo - code\executables\ (Compiled executables)
echo - code\data\       (Data files)
echo - code\            (Other code files)
echo.
echo Press any key to continue...
pause >nul
