@echo off
setlocal

set "LOG_INFO=[INFO]"
set "LOG_SUCCESS=[SUCCESS]"
set "LOG_ERROR=[ERROR]"

set CNF=%~dp0..\..\config\mysql.cnf

if not exist "%CNF%" (
    echo %LOG_ERROR% MySQL config not found. Run create_mysql_config.bat first.
    exit /b 1
)

echo %LOG_INFO% Checking MySQL connection...

mysql --defaults-extra-file="%CNF%" -s -N -e "SELECT 1;"

if errorlevel 1 (
    echo %LOG_ERROR% Failed to connect to MySQL
    exit /b 1
)

echo %LOG_SUCCESS% MySQL connection OK
exit /b 0
