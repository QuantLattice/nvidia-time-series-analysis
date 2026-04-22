@echo off
setlocal

set "LOG_INFO=[INFO]"
set "LOG_SUCCESS=[SUCCESS]"
set "LOG_ERROR=[ERROR]"

set ENV_FILE=%~dp0..\..\..\.env
set CNF_FILE=%~dp0..\..\config\mysql.cnf

if not exist "%ENV_FILE%" (
    echo %LOG_ERROR% .env not found at %ENV_FILE%
    exit /b 1
)

for /f "usebackq tokens=1,* delims==" %%A in ("%ENV_FILE%") do (
    set "%%A=%%B"
)

echo %LOG_INFO% Creating MySQL config...

(
echo [client]
echo user=%MYSQL_USER%
echo password=%MYSQL_PASSWORD%
echo host=%MYSQL_HOST%
echo port=%MYSQL_PORT%
) > "%CNF_FILE%"

if errorlevel 1 (
    echo %LOG_ERROR% Failed to write cnf
    exit /b 1
)

echo %LOG_SUCCESS% MySQL config created: %CNF_FILE%
exit /b 0
