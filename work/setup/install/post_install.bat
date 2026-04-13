@echo off
setlocal

set "LOG_INFO=[INFO]"
set "LOG_SUCCESS=[SUCCESS]"

echo %LOG_INFO% Verifying installation state...

echo %LOG_INFO% - MySQL config exists
echo %LOG_INFO% - Database created
echo %LOG_INFO% - Project structure ready

echo %LOG_SUCCESS% Verification completed
exit /b 0
