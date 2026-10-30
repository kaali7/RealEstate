@echo off
setlocal

cd /d "%~dp0"
set "PYTHON=%~dp0venv\Scripts\python.exe"
set "COUNT=%~1"

if "%COUNT%"=="" set "COUNT=100"

echo ========================================
echo GekayRealEstate demo data seeder
echo ========================================
echo.

if not exist "%PYTHON%" (
    echo Project virtual environment not found.
    echo Running the dependency installer first...
    call "%~dp0install_dependencies.bat"
    if errorlevel 1 (
        echo ERROR: Dependency setup failed.
        exit /b 1
    )
)

if not exist "%PYTHON%" (
    echo ERROR: Could not find the project Python environment.
    exit /b 1
)

echo Applying database migrations...
"%PYTHON%" "%~dp0manage.py" migrate --noinput
if errorlevel 1 (
    echo ERROR: Database migration failed.
    exit /b 1
)

echo Creating or updating %COUNT% demo listings...
"%PYTHON%" "%~dp0manage.py" seed_demo_data --count "%COUNT%"
if errorlevel 1 (
    echo ERROR: Demo data creation failed.
    exit /b 1
)

echo.
echo SUCCESS: Demo data is ready.
echo Demo images are stored in media\photos.
echo.
pause
exit /b 0

