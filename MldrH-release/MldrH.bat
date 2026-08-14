@echo off
chcp 65001 >nul
cd /d "%~dp0"
".venv\Scripts\python.exe" "MldrH.py"
if errorlevel 1 (
  echo.
  echo MldrH terminated with an error. Review the message above.
  pause
)
