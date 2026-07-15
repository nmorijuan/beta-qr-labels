#!/bin/bash

# Script para ejecutar QR Colmenas en macOS/Linux

echo ""
echo "======================================"
echo "QR Colmenas - Iniciador"
echo "======================================"
echo ""

# Verificar si venv existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar venv
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias si es necesario
if ! pip show flask &> /dev/null; then
    echo "Instalando dependencias..."
    pip install -r requirements.txt
fi

# Ejecutar verificación
echo ""
echo "Verificando setup..."
python verify_setup.py

if [ $? -ne 0 ]; then
    exit 1
fi

echo ""
echo "======================================"
echo "Iniciando QR Colmenas..."
echo "======================================"
echo ""
echo "Accede a: http://localhost:5000"
echo "Presiona Ctrl+C para detener"
echo ""

python app.py
