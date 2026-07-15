"""
Archivo de configuración de la aplicación Flask
"""

import os
from datetime import timedelta

class Config:
    """Configuración base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
    
    # Flask
    DEBUG = False
    TESTING = False
    
    # Sesión
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

class DevelopmentConfig(Config):
    """Configuración de desarrollo"""
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    """Configuración de producción"""
    DEBUG = False
    ENV = 'production'
    # En producción, cambia la SECRET_KEY
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-production')

class TestingConfig(Config):
    """Configuración de testing"""
    TESTING = True
    DEBUG = True
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'test_uploads')

# Seleccionar configuración basada en la variable de entorno
def get_config():
    env = os.environ.get('FLASK_ENV', 'development')
    
    if env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return DevelopmentConfig
