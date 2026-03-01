@echo off
setlocal

cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
  echo No se encontro el entorno virtual.
  pause
  exit /b 1
)

start "" cmd /c "timeout /t 2 /nobreak >nul && start "" http://127.0.0.1:5000/"
venv\Scripts\python.exe run.py
