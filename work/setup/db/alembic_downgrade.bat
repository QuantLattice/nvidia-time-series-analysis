@echo off
title Alembic Downgrade

setlocal
pushd %~dp0\..\..\..

set "LOG_INFO=[INFO]"
set "LOG_SUCCESS=[SUCCESS]"
set "LOG_ERROR=[ERROR]"
set "LOG_STEP=[STEP]"
set "LOG_DONE=[DONE]"

echo ======================================
echo   Alembic - Downgrade Migrations
echo ======================================
echo.

if "%~1"=="" (
    echo %LOG_STEP% No revision specified, defaulting to -1
    alembic downgrade -1
) else (
    echo %LOG_STEP% Downgrading to revision: %1
    alembic downgrade %1
)

if errorlevel 1 (
    echo %LOG_ERROR% Downgrade failed
    popd
    exit /b 1
)

echo %LOG_DONE% Downgrade completed
popd
endlocal
exit /b 0
