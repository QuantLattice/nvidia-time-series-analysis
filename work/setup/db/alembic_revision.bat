@echo off
title Alembic Migration Generator

setlocal
pushd %~dp0\..\..\..

set "LOG_INFO=[INFO]"
set "LOG_SUCCESS=[SUCCESS]"
set "LOG_ERROR=[ERROR]"
set "LOG_STEP=[STEP]"
set "LOG_DONE=[DONE]"

echo ======================================
echo   Alembic - Create New Migration
echo ======================================
echo.

if "%~1"=="" (
    echo %LOG_ERROR% Migration message is required
    echo %LOG_INFO% Example: alembic_revision.bat add_stock_quotes_table
    popd
    exit /b 1
)

echo %LOG_STEP% Generating migration...
echo %LOG_INFO% Message: %*

conda run -n nvidia-tsa alembic revision --autogenerate -m "%*"

if errorlevel 1 (
    echo %LOG_ERROR% Migration generation failed
    popd
    endlocal
    exit /b 1
)

echo %LOG_DONE% Migration created successfully
popd
endlocal
exit /b 0
