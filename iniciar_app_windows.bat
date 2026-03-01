@echo off
setlocal

cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
  echo No se encontro el entorno virtual.
  echo Ejecuta primero: python -m venv venv
  echo y luego: pip install -r requirements.txt
  pause
  exit /b 1
)

start "HCA Yoga" cmd /k "venv\Scripts\activate.bat && python run.py"
timeout /t 2 /nobreak >nul
start "" http://127.0.0.1:5000/

exit /b 0
