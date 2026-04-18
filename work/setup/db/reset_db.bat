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

echo %LOG_INFO% Dropping MySQL database...

mysql --defaults-extra-file="%CNF%" ^
-e "DROP DATABASE IF EXISTS `nvidia_timeseries`;"

if errorlevel 1 (
    echo %LOG_ERROR% Failed to drop database
    exit /b 1
)

echo %LOG_SUCCESS% Database dropped successfully
exit /b 0
