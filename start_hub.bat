@echo off
setlocal

cd /d "%~dp0"

if exist "C:\Users\pilep\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
    "C:\Users\pilep\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" serve_hub.py
    goto :eof
)

where py >nul 2>nul
if %errorlevel%==0 (
    py serve_hub.py
    goto :eof
)

where python >nul 2>nul
if %errorlevel%==0 (
    python serve_hub.py
    goto :eof
)

echo Could not find a Python runtime to start the SciCopilot hub.
echo Install Python or update start_hub.bat with your Python path.
pause
