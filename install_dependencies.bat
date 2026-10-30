@echo off
setlocal

cd /d "%~dp0"
set "VENV=%~dp0venv"
set "PYTHON=%VENV%\Scripts\python.exe"

echo ========================================
echo GekayRealEstate dependency installer
echo ========================================
echo.

if not exist "%PYTHON%" (
    echo Virtual environment not found.
    echo Creating it with Python 3.14...
    py -3.14 -m venv "%VENV%"
    if errorlevel 1 (
        echo ERROR: Could not create the virtual environment.
        echo Make sure Python 3.14 is installed and available through the py launcher.
        exit /b 1
    )
    echo Virtual environment created.
    echo.
)

if not exist "%PYTHON%" (
    echo ERROR: The virtual environment Python executable was not created.
    exit /b 1
)

echo Checking pip...
"%PYTHON%" -m pip --version >nul 2>&1
if errorlevel 1 (
    echo pip is not available. Installing pip...
    "%PYTHON%" -m ensurepip --upgrade
    if errorlevel 1 (
        echo ERROR: Could not install pip.
        exit /b 1
    )
)

echo Installing missing or outdated packages from requirements.txt...
"%PYTHON%" -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 (
    echo ERROR: Dependency installation failed.
    exit /b 1
)

echo.
echo Verifying installed package dependencies...
"%PYTHON%" -m pip check
if errorlevel 1 (
    echo ERROR: Package verification failed.
    exit /b 1
)

echo.
echo Checking Django configuration...
"%PYTHON%" "%~dp0manage.py" check
if errorlevel 1 (
    echo ERROR: Django configuration check failed.
    exit /b 1
)

echo.
echo Applying database migrations...
"%PYTHON%" "%~dp0manage.py" migrate --noinput
if errorlevel 1 (
    echo ERROR: Database migration failed.
    exit /b 1
)

echo.
echo SUCCESS: All dependencies are installed and verified.
echo Virtual environment: %VENV%
echo.
pause
exit /b 0

