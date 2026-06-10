@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo  NVIDIA Time Series Analysis — Installation
echo ============================================================
echo.

:: ---------------------------------------------------------------
:: 1. Locate conda
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

echo [ERROR] Anaconda / Miniconda not found.
echo.
echo Please install Anaconda from https://www.anaconda.com/download
echo and re-run this script.
echo.
pause
exit /b 1

:found_conda
echo [OK] Conda found: %CONDA_ROOT%

:: Initialize conda for this cmd session
call "%CONDA_ROOT%\Scripts\activate.bat" >nul 2>&1

:: ---------------------------------------------------------------
:: 2. Create or update the conda environment
:: ---------------------------------------------------------------
set ENV_NAME=nvidia-tsa

echo.
conda env list | findstr /C:"%ENV_NAME%" >nul 2>&1
if not errorlevel 1 (
    echo [INFO] Environment "%ENV_NAME%" already exists. Skipping creation.
) else (
    echo Creating conda environment "%ENV_NAME%" (cloning base)...
    call conda create -n %ENV_NAME% --clone base -y
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to create the conda environment.
        pause
        exit /b 1
    )
)

:: ---------------------------------------------------------------
:: 3. Install Python packages via pip
:: ---------------------------------------------------------------
set ENV_PIP=%CONDA_ROOT%\envs\%ENV_NAME%\Scripts\pip.exe

echo.
echo Installing packages from requirements.txt...
call "%ENV_PIP%" install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install packages.
    echo Check your internet connection and try again.
    echo.
    pause
    exit /b 1
)

:: ---------------------------------------------------------------
:: 4. Set up .env if it does not exist
:: ---------------------------------------------------------------
if not exist .env (
    if exist .env.example (
        echo.
        echo Copying .env.example to .env...
        copy .env.example .env >nul
        echo [NOTE] Open .env and set your MySQL credentials before running.
    )
)

:: ---------------------------------------------------------------
:: Done
:: ---------------------------------------------------------------
echo.
echo ============================================================
echo  Installation complete!
echo ============================================================
echo.
echo  To start the application run:  run.bat
echo.
pause
exit /b 0
