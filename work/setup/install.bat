@echo off
title NVIDIA Project Installation

setlocal
pushd %~dp0

set "LOG_INFO=[INFO]"
set "LOG_SUCCESS=[SUCCESS]"
set "LOG_ERROR=[ERROR]"
set "LOG_STEP=[STEP]"
set "LOG_DONE=[DONE]"

echo ======================================
echo   NVIDIA Stock Analyzer Setup
echo ======================================
echo.

echo %LOG_STEP% Step 1: Preparing MySQL config...
call db\create_mysql_config.bat
if errorlevel 1 (
    echo %LOG_ERROR% Failed to create MySQL config
    popd
    exit /b 1
)
echo %LOG_SUCCESS% MySQL config created

echo.
echo %LOG_STEP% Step 2: Checking MySQL connection...
call db\check_mysql.bat
if errorlevel 1 (
    echo %LOG_ERROR% MySQL connection failed or config invalid
    popd
    exit /b 1
)
echo %LOG_SUCCESS% MySQL connection OK

echo.
echo %LOG_STEP% Step 3: Initializing database...
call db\init_db.bat
if errorlevel 1 (
    echo %LOG_ERROR% Database initialization failed
    popd
    exit /b 1
)
echo %LOG_SUCCESS% Database initialized

echo.
echo %LOG_STEP% Step 4: Final verification...
call install\post_install.bat
if errorlevel 1 (
    echo %LOG_ERROR% Post-install checks failed
    popd
    exit /b 1
)
echo %LOG_SUCCESS% System verification passed

echo.
echo %LOG_DONE% Setup completed successfully!
echo %LOG_INFO% You can now run the application using main.py

popd
endlocal
exit /b 0
