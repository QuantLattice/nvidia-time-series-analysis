@echo off
title Alembic Upgrade

setlocal
pushd %~dp0\..\..\..

set "LOG_INFO=[INFO]"
set "LOG_SUCCESS=[SUCCESS]"
set "LOG_ERROR=[ERROR]"
set "LOG_STEP=[STEP]"
set "LOG_DONE=[DONE]"

echo ======================================
echo   Alembic - Apply Migrations
echo ======================================
echo.

echo %LOG_STEP% Upgrading database to HEAD...

alembic upgrade head

if errorlevel 1 (
    echo %LOG_ERROR% Upgrade failed
    popd
    exit /b 1
)

echo %LOG_DONE% Database successfully upgraded
popd
endlocal
exit /b 0
