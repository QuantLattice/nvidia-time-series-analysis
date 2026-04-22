@echo off
setlocal

set "LOG_INFO=[INFO]"
set "LOG_SUCCESS=[SUCCESS]"

echo %LOG_INFO% Clearing generated files...

del /q "%~dp0..\..\output\*" 2>nul
del /q "%~dp0..\..\graphics\*" 2>nul
del /q "%~dp0..\..\logs\*" 2>nul

echo %LOG_SUCCESS% Generated files cleared
exit /b 0
