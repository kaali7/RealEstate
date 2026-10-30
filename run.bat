@echo off
setlocal

cd /d "%~dp0"
set "VENV=%~dp0venv"
set "PYTHON=%VENV%\Scripts\python.exe"

echo ===================================================
echo Starting GekayRealEstate Application Server
echo ===================================================
echo.

:: 1. Check or create virtual environment
echo [1/7] Checking Python environment...
if not exist "%PYTHON%" (
    echo Virtual environment not found. Locating Python...
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
        echo Please install Python 3.14 or run install_dependencies.bat first.
        exit /b 1
    )

    echo Creating virtual environment using %BOOT_PY%...
    %BOOT_PY% -m venv "%VENV%"
    if errorlevel 1 (
        echo ERROR: Failed to create the virtual environment.
        exit /b 1
    )
)

:: 2. Ensure default .env exists for local development
if not exist "%~dp0.env" (
    echo [2/7] Creating default local .env file...
    (
        echo DJANGO_SECRET_KEY=dev-local-secret-key-gekay-realestate-2026
        echo DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
    ) > "%~dp0.env"
) else (
    echo [2/7] Local environment configuration verified.
)

:: 3. Validate packages
echo [3/7] Validating dependencies...
"%PYTHON%" -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 (
    echo ERROR: Dependency installation failed.
    exit /b 1
)

"%PYTHON%" -m pip check
if errorlevel 1 (
    echo ERROR: Dependency check failed.
    exit /b 1
)

:: 4. Django configuration check
echo [4/7] Checking Django configuration...
"%PYTHON%" "%~dp0manage.py" check
if errorlevel 1 (
    echo ERROR: Django configuration check failed.
    exit /b 1
)

:: 5. Database migrations
echo [5/7] Applying database migrations...
"%PYTHON%" "%~dp0manage.py" migrate --noinput
if errorlevel 1 (
    echo ERROR: Database migration failed.
    exit /b 1
)

:: 6. Automated tests
echo [6/7] Running automated test suite...
"%PYTHON%" "%~dp0manage.py" test
if errorlevel 1 (
    echo ERROR: Automated tests failed. Server startup aborted.
    exit /b 1
)

:: 7. Check if demo listings exist, auto-seed if database is empty
echo [7/7] Checking property catalog data...
"%PYTHON%" -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangofirst.settings'); django.setup(); from listings.models import Listing; exit(0 if Listing.objects.exists() else 1)" >nul 2>&1
if errorlevel 1 (
    echo Database has no listings. Auto-seeding 100 demo properties...
    "%PYTHON%" "%~dp0manage.py" seed_demo_data --count 100
) else (
    echo Property catalog is ready.
)

echo.
echo ===================================================
echo All checks passed successfully!
echo Starting Django development server at:
echo    http://127.0.0.1:8000/
echo.
echo Press Ctrl+C in this window to stop the server.
echo ===================================================
echo.
"%PYTHON%" "%~dp0manage.py" runserver 127.0.0.1:8000

endlocal
