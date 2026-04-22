@echo off
title Apply Alembic Migrations

setlocal
pushd %~dp0..\..\..\

echo [STEP] Applying database migrations...
alembic upgrade head

if errorlevel 1 (
    echo [ERROR] Failed to apply migrations
    popd
    exit /b 1
)

echo [SUCCESS] Migrations applied successfully
popd
endlocal
exit /b 0
