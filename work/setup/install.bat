@echo off
title NVIDIA Stock Analyzer — Installation
setlocal enabledelayedexpansion

set "LOG_INFO=[INFO]"
set "LOG_SUCCESS=[SUCCESS]"
set "LOG_ERROR=[ERROR]"
set "LOG_STEP=[STEP]"
set "LOG_DONE=[DONE]"

echo ======================================
echo   NVIDIA Stock Analyzer — Setup
echo ======================================
echo.

:: ---------------------------------------------------------------
:: Step 0: Locate Anaconda / Miniconda
:: ---------------------------------------------------------------
set CONDA_ROOT=

where conda >nul 2>&1
if not errorlevel 1 (
    for /f "delims=" %%i in ('conda info --base 2^>nul') do set CONDA_ROOT=%%i
    if defined CONDA_ROOT goto :found_conda
)

for %%p in (
    "%USERPROFILE%\anaconda3"
    "%USERPROFILE%\Anaconda3"
    "%USERPROFILE%\miniconda3"
    "%USERPROFILE%\Miniconda3"
    "C:\ProgramData\Anaconda3"
    "C:\ProgramData\anaconda3"
    "C:\Anaconda3"
    "C:\anaconda3"
    "C:\ProgramData\miniconda3"
    "C:\miniconda3"
) do (
    if exist "%%~p\Scripts\conda.exe" (
        set CONDA_ROOT=%%~p
        goto :found_conda
    )
)

echo %LOG_ERROR% Anaconda / Miniconda not found.
echo.
echo Please install Anaconda from https://www.anaconda.com/download
echo and re-run this script.
echo.
pause
exit /b 1

:found_conda
echo %LOG_SUCCESS% Conda found: %CONDA_ROOT%
call "%CONDA_ROOT%\Scripts\activate.bat" >nul 2>&1

:: ---------------------------------------------------------------
:: Step 1: Create or update the conda environment
:: ---------------------------------------------------------------
echo.
echo %LOG_STEP% Step 1: Setting up conda environment "nvidia-tsa"...

conda env list | findstr /C:"nvidia-tsa" >nul 2>&1
if not errorlevel 1 (
    echo %LOG_INFO% Environment "nvidia-tsa" already exists — skipping creation
    goto :env_ready
)

echo %LOG_INFO% Cloning base environment into "nvidia-tsa"...
call conda create -n nvidia-tsa --clone base -y

if errorlevel 1 (
    echo %LOG_ERROR% Failed to clone base environment
    pause
    exit /b 1
)

:env_ready
echo %LOG_SUCCESS% Conda environment ready

:: ---------------------------------------------------------------
:: Step 2: Prepare MySQL config
:: ---------------------------------------------------------------
echo.
echo %LOG_STEP% Step 2: Preparing MySQL config...
pushd %~dp0
call db\create_mysql_config.bat
if errorlevel 1 (
    echo %LOG_ERROR% Failed to create MySQL config
    popd
    pause
    exit /b 1
)
echo %LOG_SUCCESS% MySQL config created

:: ---------------------------------------------------------------
:: Step 3: Check MySQL connection
:: ---------------------------------------------------------------
echo.
echo %LOG_STEP% Step 3: Checking MySQL connection...
call db\check_mysql.bat
if errorlevel 1 (
    echo %LOG_ERROR% MySQL connection failed — check credentials in config\mysql.cnf
    popd
    pause
    exit /b 1
)
echo %LOG_SUCCESS% MySQL connection OK

:: ---------------------------------------------------------------
:: Step 4: Initialize database
:: ---------------------------------------------------------------
echo.
echo %LOG_STEP% Step 4: Initializing database...
call db\init_db.bat
if errorlevel 1 (
    echo %LOG_ERROR% Database initialization failed
    popd
    pause
    exit /b 1
)
echo %LOG_SUCCESS% Database initialized

:: ---------------------------------------------------------------
:: Step 5: Apply database migrations
:: ---------------------------------------------------------------
echo.
echo %LOG_STEP% Step 5: Applying database migrations...
call db\apply_migrations.bat
if errorlevel 1 (
    echo %LOG_ERROR% Database migrations failed
    popd
    pause
    exit /b 1
)
echo %LOG_SUCCESS% Migrations applied

:: ---------------------------------------------------------------
:: Step 6: Final verification
:: ---------------------------------------------------------------
echo.
echo %LOG_STEP% Step 6: Verifying installation...
call install\post_install.bat
if errorlevel 1 (
    echo %LOG_ERROR% Post-install checks failed
    popd
    pause
    exit /b 1
)
echo %LOG_SUCCESS% Verification passed

popd
echo.
echo %LOG_DONE% Setup completed successfully!
echo %LOG_INFO% Launch the application with:  run.bat
echo.
pause
endlocal
exit /b 0
