@echo off
REM Script para inicializar el repositorio Git y subirlo a GitHub

echo.
echo ======================================
echo QR Colmenas - Inicializador de GitHub
echo ======================================
echo.

REM Verificar si Git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git no está instalado. Descargarlo desde https://git-scm.com/
    pause
    exit /b 1
)

REM Inicializar repositorio Git
echo ✓ Inicializando repositorio Git...
git init

echo ✓ Configurando usuario de Git...
git config user.email "tu.email@example.com"
git config user.name "Tu Nombre"

REM Agregar todos los archivos
echo ✓ Agregando archivos...
git add .

REM Crear commit inicial
echo ✓ Creando commit inicial...
git commit -m "Initial commit: QR Colmenas Web App"

REM Cambiar rama a main si es necesario
git branch -M main

echo.
echo ======================================
echo Pasos siguientes:
echo ======================================
echo.
echo 1. Crea un nuevo repositorio en GitHub:
echo    https://github.com/new
echo.
echo 2. Cuando crees el repositorio, copia la URL
echo.
echo 3. Ejecuta este comando en la terminal:
echo    git remote add origin https://github.com/TU_USUARIO/QR-Colmenas-Web.git
echo.
echo 4. Sube el código a GitHub:
echo    git push -u origin main
echo.
echo 5. ¡Listo! Tu repositorio está en GitHub
echo.
echo ======================================
echo.
pause
