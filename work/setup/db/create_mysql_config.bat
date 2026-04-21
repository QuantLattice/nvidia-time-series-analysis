@echo off
setlocal
pushd "%~dp0\..\..\.."

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py -3 -m work.setup.setup_manager create-mysql-config %*
) else (
    python -m work.setup.setup_manager create-mysql-config %*
)
set "EXIT_CODE=%ERRORLEVEL%"

popd
endlocal
exit /b %EXIT_CODE%
