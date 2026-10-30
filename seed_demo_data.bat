@echo off
setlocal

cd /d "%~dp0"
set "VENV=%~dp0venv"
set "PYTHON=%VENV%\Scripts\python.exe"
set "COUNT=%~1"

if "%COUNT%"=="" set "COUNT=100"

echo ===================================================
echo GekayRealEstate Demo Data Seeder
echo ===================================================
echo.

if not exist "%PYTHON%" (
    echo Virtual environment not found. Running installer first...
    call "%~dp0install_dependencies.bat"
    if errorlevel 1 (
        echo ERROR: Dependency setup failed.
        exit /b 1
    )
)

if not exist "%PYTHON%" (
    echo ERROR: Python executable not found at "%PYTHON%".
    exit /b 1
)

:: Ensure default .env exists
if not exist "%~dp0.env" (
    echo Creating default local .env file...
    (
        echo DJANGO_SECRET_KEY=dev-local-secret-key-gekay-realestate-2026
        echo DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
    ) > "%~dp0.env"
)

:: Apply database migrations first
echo Applying database migrations...
"%PYTHON%" "%~dp0manage.py" migrate --noinput
if errorlevel 1 (
    echo ERROR: Database migration failed.
    exit /b 1
)

:: Seed or update demo data
echo.
echo Seeding or refreshing %COUNT% demo listings with 1-5 bedrooms and amenities...
"%PYTHON%" "%~dp0manage.py" seed_demo_data --count "%COUNT%"
if errorlevel 1 (
    echo ERROR: Demo data creation failed.
    exit /b 1
)

echo.
echo ===================================================
echo SUCCESS: Demo listings and realtors are ready!
echo - Listings seeded: %COUNT%
echo - Bedrooms: 1 to 5 BHK distributed evenly
echo - Cities: Mumbai, Pune, Thane, Nashik
echo - Amenities: swimming pool, garage, balcony, garden, terrace
echo - Media assets stored in: media\photos\
echo ===================================================
echo.
pause
exit /b 0
