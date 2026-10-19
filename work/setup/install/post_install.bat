@echo off
setlocal

set "LOG_INFO=[INFO]"
set "LOG_SUCCESS=[SUCCESS]"
set "LOG_ERROR=[ERROR]"
set "LOG_STEP=[STEP]"

echo %LOG_STEP% Running post-install verification...
echo.

:: ---------------------------------------------------------------
:: Check 1: conda environment exists
:: ---------------------------------------------------------------
echo %LOG_INFO% Checking conda environment "nvidia-tsa"...
conda env list | findstr /C:"nvidia-tsa" >nul 2>&1
if errorlevel 1 (
    echo %LOG_ERROR% Conda environment "nvidia-tsa" not found
    exit /b 1
)
echo %LOG_SUCCESS% Conda environment exists

:: ---------------------------------------------------------------
:: Check 2: Python is accessible in the environment
:: ---------------------------------------------------------------
echo %LOG_INFO% Checking Python in "nvidia-tsa"...
conda run -n nvidia-tsa python --version >nul 2>&1
if errorlevel 1 (
    echo %LOG_ERROR% Python is not accessible in environment "nvidia-tsa"
    exit /b 1
)
echo %LOG_SUCCESS% Python is accessible

:: ---------------------------------------------------------------
:: Check 3: Alembic migration status
:: ---------------------------------------------------------------
echo %LOG_INFO% Checking database migration state...
pushd %~dp0..\..\..
conda run -n nvidia-tsa alembic current >nul 2>&1
if errorlevel 1 (
    echo %LOG_ERROR% Could not read alembic revision — database may not be initialised
    popd
    exit /b 1
)
popd
echo %LOG_SUCCESS% Database schema is up to date

:: ---------------------------------------------------------------
:: Check 4: Key project directories exist
:: ---------------------------------------------------------------
echo %LOG_INFO% Checking project structure...
set "PROJECT_ROOT=%~dp0..\..\..\"
if not exist "%PROJECT_ROOT%work\scripts\" (
    echo %LOG_ERROR% work\scripts directory is missing
    exit /b 1
)
if not exist "%PROJECT_ROOT%alembic.ini" (
    echo %LOG_ERROR% alembic.ini is missing from project root
    exit /b 1
)
echo %LOG_SUCCESS% Project structure is intact

echo.
echo %LOG_SUCCESS% All checks passed — installation is complete
endlocal
exit /b 0
