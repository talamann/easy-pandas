@echo off
REM Quick setup script for publishing easy_pandas to PyPI

echo ========================================
echo Easy Pandas - PyPI Publishing Setup
echo ========================================
echo.

echo Step 1: Installing required tools...
pip install --upgrade pip build twine
echo.

echo Step 2: Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist easy_pandas.egg-info rmdir /s /q easy_pandas.egg-info
echo.

echo Step 3: Building the package...
python -m build
echo.

echo Step 4: Checking distribution files...
python -m twine check dist/*
echo.

echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Your package files are in the 'dist' folder:
dir dist
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Test on TestPyPI (recommended):
echo    python -m twine upload --repository testpypi dist/*
echo.
echo 2. Publish to PyPI:
echo    python -m twine upload dist/*
echo.
echo See PUBLISHING.md for detailed instructions.
echo.
pause
