import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env si existe
load_dotenv()

class Config:
    """
    Configuración de la aplicación usando variables de entorno
    
    Para configurar:
    1. Crea un archivo .env basado en .env.example
    2. O configura las variables de entorno en tu sistema
    """
    
    # Configuración de la base de datos SQL Server
    DB_SERVER = os.environ.get('DB_SERVER') or 'localhost'
    DB_NAME = os.environ.get('DB_NAME') or 'database_name'
    DB_USER = os.environ.get('DB_USER') or 'username'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'password'
    
    # Configuración de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'True').lower() in ['true', '1', 'yes']
    
    # Configuración de búsqueda
    DEFAULT_SEARCH_DAYS = int(os.environ.get('DEFAULT_SEARCH_DAYS', '365'))
    
    @classmethod
    def validate_config(cls):
        """Valida que las configuraciones críticas estén presentes"""
        required_vars = ['DB_SERVER', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
        missing_vars = []
        
        for var in required_vars:
            if not getattr(cls, var) or getattr(cls, var) in ['localhost', 'database_name', 'username', 'password']:
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Configuración incompleta. Variables faltantes o con valores por defecto: {', '.join(missing_vars)}")
        
        return True