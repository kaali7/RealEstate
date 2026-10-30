@echo off
setlocal

cd /d "%~dp0"
set "PYTHON=%~dp0venv\Scripts\python.exe"

echo [1/6] Checking Python environment...
if not exist "%PYTHON%" (
    echo Virtual environment not found. Creating it...
    py -3.14 -m venv "%~dp0venv"
    if errorlevel 1 (
        echo ERROR: Could not create the virtual environment.
        exit /b 1
    )
)

echo [2/6] Installing or validating dependencies...
"%PYTHON%" -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Dependency installation failed.
    exit /b 1
)

"%PYTHON%" -m pip check
if errorlevel 1 (
    echo ERROR: Dependency check failed.
    exit /b 1
)

echo [3/6] Checking Django configuration...
"%PYTHON%" manage.py check
if errorlevel 1 (
    echo ERROR: Django configuration check failed.
    exit /b 1
)

echo [4/6] Applying database migrations...
"%PYTHON%" manage.py migrate --noinput
if errorlevel 1 (
    echo ERROR: Database migration failed.
    exit /b 1
)

echo [5/6] Running automated tests...
"%PYTHON%" manage.py test
if errorlevel 1 (
    echo ERROR: Automated tests failed. Server was not started.
    exit /b 1
)

echo [6/6] All checks passed.
echo Starting Django at http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server.
"%PYTHON%" manage.py runserver 127.0.0.1:8000

endlocal
