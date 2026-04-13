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

echo %LOG_INFO% Creating MySQL database...

mysql --defaults-extra-file="%CNF%" ^
-e "CREATE DATABASE IF NOT EXISTS `nvidia_timeseries` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

if errorlevel 1 (
    echo %LOG_ERROR% Failed to create database
    exit /b 1
)

echo %LOG_SUCCESS% Database created successfully
exit /b 0
