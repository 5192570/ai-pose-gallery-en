@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if not errorlevel 1 (
    py -3 scripts\serve.py
    goto :end
)

where python >nul 2>nul
if not errorlevel 1 (
    python scripts\serve.py
    goto :end
)

echo Python 3 was not found.
echo Install Python 3 from https://www.python.org/downloads/ and try again.
pause
exit /b 1

:end
if errorlevel 1 pause
endlocal
