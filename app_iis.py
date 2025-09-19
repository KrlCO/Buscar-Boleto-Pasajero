#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import logging
from datetime import datetime

# Agregar el directorio actual al path de Python
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Configurar logging para IIS
log_dir = os.path.join(current_dir, 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'iis_app.log'), encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

try:
    # Importar la aplicación Flask principal
    from app import app
    
    logger.info("=" * 50)
    logger.info("Iniciando aplicación en IIS")
    logger.info(f"Servidor: ")
    logger.info(f"Sistema: ")
    logger.info(f"IP: ")
    logger.info(f"Directorio: {current_dir}")
    logger.info(f"Python Path: {sys.path[0]}")
    logger.info("Aplicación optimizada para búsquedas del año 2025")
    logger.info("=" * 50)
    
    # Configuración específica para IIS
    app.config['DEBUG'] = False
    app.config['TESTING'] = False
    
    # Configurar headers de seguridad para IIS
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Server'] = 'IIS/BuscaDatosPasajero'
        return response
    
    # Log de inicio exitoso
    logger.info("Aplicación Flask cargada exitosamente para IIS")
    
except Exception as e:
    logger.error(f"Error al cargar la aplicación: {str(e)}")
    logger.error(f"Directorio actual: {current_dir}")
    logger.error(f"Python path: {sys.path}")
    raise

# Punto de entrada para IIS con FastCGI
if __name__ == '__main__':
    try:
        logger.info("Iniciando aplicación en modo desarrollo (no recomendado para producción)")
        app.run(
            debug=False,
            host='0.0.0.0',
            port=5000
        )
    except Exception as e:
        logger.error(f"Error al iniciar aplicación: {str(e)}")
        raise

# Exportar la aplicación para FastCGI
# Esta es la variable que IIS/FastCGI utilizará
application = app

# Información adicional para debugging
def get_app_info():
    """Función de utilidad para obtener información de la aplicación"""
    return {
        'app_name': 'Búsqueda de Datos de Pasajeros',
        'version': '1.0.0',
        'server': '',
        'os': '',
        'ip': '',
        'deployment': 'IIS with FastCGI',
        'python_version': sys.version,
        'current_dir': current_dir,
        'optimized_for': '2025 passenger data searches'
    }

# Log de información de la aplicación al cargar
if __name__ != '__main__':
    info = get_app_info()
    logger.info(f"App Info: {info['app_name']} v{info['version']}")
    logger.info(f"Deployment: {info['deployment']} on {info['server']}")