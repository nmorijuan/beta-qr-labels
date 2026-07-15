#!/usr/bin/env python3
"""
Script de verificación y setup rápido para QR Colmenas
"""

import os
import sys
import subprocess

def print_header(text):
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50 + "\n")

def check_python():
    """Verificar versión de Python"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor} (OK)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} (Requiere 3.8+)")
        return False

def check_files():
    """Verificar estructura de archivos"""
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/index.html',
        'static/style.css',
        'static/script.js',
        'src/generar_zpl_web.py',
        'README.md'
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} (No encontrado)")
            all_ok = False
    
    return all_ok

def check_dependencies():
    """Verificar dependencias instaladas"""
    try:
        import flask
        print(f"✓ Flask {flask.__version__}")
    except ImportError:
        print("✗ Flask no instalado")
        return False
    
    try:
        import pandas
        print(f"✓ Pandas {pandas.__version__}")
    except ImportError:
        print("✗ Pandas no instalado")
        return False
    
    try:
        import openpyxl
        print(f"✓ Openpyxl {openpyxl.__version__}")
    except ImportError:
        print("✗ Openpyxl no instalado")
        return False
    
    return True

def create_directories():
    """Crear directorios necesarios"""
    dirs = ['uploads', 'output']
    for dir_name in dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"✓ Directorio '{dir_name}' creado")
        else:
            print(f"✓ Directorio '{dir_name}' existe")

def main():
    print_header("QR Colmenas - Verificación de Setup")
    
    print("1. Verificando Python...")
    if not check_python():
        sys.exit(1)
    
    print("\n2. Verificando estructura de archivos...")
    if not check_files():
        print("\n⚠️  Algunos archivos no se encontraron")
        sys.exit(1)
    
    print("\n3. Verificando dependencias...")
    if not check_dependencies():
        print("\n✗ Dependencias no instaladas")
        print("Ejecuta: pip install -r requirements.txt")
        sys.exit(1)
    
    print("\n4. Creando directorios...")
    create_directories()
    
    print_header("✓ Todo OK - Listo para iniciar")
    
    print("Para iniciar la aplicación, ejecuta:")
    print("  python app.py")
    print("\nO con gunicorn:")
    print("  gunicorn --bind 0.0.0.0:5000 wsgi:app")
    print("\nAccede a: http://localhost:5000")
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelado por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
