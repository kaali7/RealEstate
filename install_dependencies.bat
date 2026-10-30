@echo off
setlocal

cd /d "%~dp0"
set "VENV=%~dp0venv"
set "PYTHON=%VENV%\Scripts\python.exe"

echo ===================================================
echo GekayRealEstate Dependency Installer and Environment Setup
echo ===================================================
echo.

:: 1. Check or create virtual environment
if not exist "%PYTHON%" (
    echo [1/6] Virtual environment not found. Locating Python...
    set "BOOT_PY="
    py -3.14 -c "import sys; exit(0)" >nul 2>&1 && set "BOOT_PY=py -3.14"
    if not defined BOOT_PY (
        py -3 -c "import sys; exit(0)" >nul 2>&1 && set "BOOT_PY=py -3"
    )
    if not defined BOOT_PY (
        python -c "import sys; exit(0)" >nul 2>&1 && set "BOOT_PY=python"
    )

    if not defined BOOT_PY (
        echo ERROR: No Python interpreter was found on your system.
        echo Please install Python 3.14 or make sure python is added to your PATH.
        exit /b 1
    )

    echo Creating virtual environment using %BOOT_PY%...
    %BOOT_PY% -m venv "%VENV%"
    if errorlevel 1 (
        echo ERROR: Failed to create the virtual environment at "%VENV%".
        exit /b 1
    )
    echo Virtual environment created successfully.
) else (
    echo [1/6] Virtual environment verified at: %VENV%
)

if not exist "%PYTHON%" (
    echo ERROR: Python executable not found at "%PYTHON%".
    exit /b 1
)

:: 2. Ensure default .env exists for local development
echo [2/6] Checking local environment configuration (.env)...
if not exist "%~dp0.env" (
    echo Creating default local .env file...
    (
        echo DJANGO_SECRET_KEY=dev-local-secret-key-gekay-realestate-2026
        echo DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
    ) > "%~dp0.env"
    echo Created "%~dp0.env" with default local settings.
) else (
    echo Local .env file is present.
)

:: Ensure media\photos directory exists
if not exist "%~dp0media\photos" (
    mkdir "%~dp0media\photos" >nul 2>&1
)

:: 3. Check and install/update pip
echo [3/6] Checking pip package manager...
"%PYTHON%" -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Installing pip...
    "%PYTHON%" -m ensurepip --upgrade
    if errorlevel 1 (
        echo ERROR: Could not bootstrap pip in the virtual environment.
        exit /b 1
    )
)

:: 4. Install dependencies from requirements.txt
echo [4/6] Installing packages from requirements.txt...
"%PYTHON%" -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 (
    echo ERROR: Dependency installation failed.
    exit /b 1
)

echo Verifying installed package dependencies...
"%PYTHON%" -m pip check
if errorlevel 1 (
    echo ERROR: Dependency consistency check failed.
    exit /b 1
)

:: 5. Validate Django configuration
echo [5/6] Validating Django configuration...
"%PYTHON%" "%~dp0manage.py" check
if errorlevel 1 (
    echo ERROR: Django configuration check failed.
    exit /b 1
)

:: 6. Apply database migrations
echo [6/6] Applying database migrations...
"%PYTHON%" "%~dp0manage.py" migrate --noinput
if errorlevel 1 (
    echo ERROR: Database migration failed.
    exit /b 1
)

echo.
echo ===================================================
echo SUCCESS: All dependencies and migrations are ready!
echo Virtual environment: %VENV%
echo You can now start the server with: run.bat
echo Or seed sample data with: seed_demo_data.bat
echo ===================================================
echo.
pause
exit /b 0
