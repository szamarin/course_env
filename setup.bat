@echo off
REM ============================================================================
REM Course Environment Setup Wrapper for Windows Command Prompt / Double-Click
REM ============================================================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1" %*
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Setup encountered an error. Please review the messages above.
    exit /b %ERRORLEVEL%
)
