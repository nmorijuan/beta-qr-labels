"""
Configuración para ejecutar con gunicorn (producción)
"""

import os
import sys

# Agregar la carpeta al path
sys.path.insert(0, os.path.dirname(__file__))

from app import app

if __name__ == "__main__":
    app.run()
