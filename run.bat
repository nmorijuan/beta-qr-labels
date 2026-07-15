@echo off
REM Script para ejecutar QR Colmenas en Windows

echo.
echo ======================================
echo QR Colmenas - Iniciador
echo ======================================
echo.

REM Verificar si venv existe
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar venv
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias si es necesario
python -m pip --version >nul 2>&1
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
)

REM Ejecutar verificación
echo.
echo Verificando setup...
python verify_setup.py

if errorlevel 1 (
    pause
    exit /b 1
)

echo.
echo ======================================
echo Iniciando QR Colmenas...
echo ======================================
echo.
echo Accede a: http://localhost:5000
echo Presiona Ctrl+C para detener
echo.

python app.py

pause
