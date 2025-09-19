import os

class Config:
    # Configuración de la base de datos SQL Server
    DB_SERVER = ''
    DB_NAME = ''
    DB_USER = ''
    DB_PASSWORD = ''
    
    # Configuración de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    
    # Configuración de búsqueda
    DEFAULT_SEARCH_DAYS = 365