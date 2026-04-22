@echo off
title NVIDIA Project Reset Tool

setlocal
pushd %~dp0

set "LOG_INFO=[INFO]"
set "LOG_SUCCESS=[SUCCESS]"
set "LOG_WARNING=[WARNING]"
set "LOG_ERROR=[ERROR]"
set "LOG_STEP=[STEP]"
set "LOG_DONE=[DONE]"

echo ======================================
echo   NVIDIA Project Reset Tool
echo ======================================
echo.

echo %LOG_WARNING% This will reset all project data!
echo.

set /p confirm=Type YES to continue: 

if /i not "%confirm%"=="YES" (
    echo %LOG_INFO% Reset cancelled by user
    popd
    exit /b 0
)

echo.
echo %LOG_STEP% Preparing MySQL config...
call db\create_mysql_config.bat
if errorlevel 1 (
    echo %LOG_ERROR% Failed to create MySQL config
    popd
    exit /b 1
)
echo %LOG_SUCCESS% Config ready

echo.
echo %LOG_STEP% Dropping database...
call db\reset_db.bat
if errorlevel 1 (
    echo %LOG_ERROR% Database reset failed
    popd
    exit /b 1
)
echo %LOG_SUCCESS% Database dropped

echo.
echo %LOG_STEP% Clearing generated files...
call reset\clear_files.bat
if errorlevel 1 (
    echo %LOG_ERROR% Failed to clear files
    popd
    exit /b 1
)
echo %LOG_SUCCESS% Workspace cleaned

echo.
echo %LOG_DONE% Reset completed successfully

popd
endlocal
exit /b 0
