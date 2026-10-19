@echo off
title Alembic Current Revision

setlocal
pushd %~dp0\..\..\..

set "LOG_INFO=[INFO]"
set "LOG_STEP=[STEP]"

echo ======================================
echo   Alembic - Current Revision
echo ======================================
echo.

echo %LOG_STEP% Checking current DB revision...
conda run -n nvidia-tsa alembic current

popd
endlocal
exit /b 0
