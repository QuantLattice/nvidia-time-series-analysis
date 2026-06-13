@echo off
setlocal enabledelayedexpansion

:: ---------------------------------------------------------------
:: Locate Anaconda / Miniconda
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

echo [ERROR] Anaconda / Miniconda not found. Run install.bat first.
pause
exit /b 1

:found_conda
:: Activate the project environment
call "%CONDA_ROOT%\Scripts\activate.bat" >nul 2>&1
call conda activate nvidia-tsa >nul 2>&1

:: Verify activation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Could not activate environment "nvidia-tsa".
    echo Run install.bat to create it.
    pause
    exit /b 1
)

:: ---------------------------------------------------------------
:: Change to project root and launch the application
:: ---------------------------------------------------------------
pushd %~dp0..\..
echo Starting NVIDIA Time Series Analysis...
echo.
python -m work.scripts.main

if errorlevel 1 (
    echo.
    echo [ERROR] Application exited with an error. See output above.
    popd
    pause
    endlocal
    exit /b 1
)

popd
endlocal
exit /b 0
