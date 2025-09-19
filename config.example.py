import os

class Config:
    """
    Configuración de ejemplo para la aplicación Buscar Boleto Pasajero
    
    INSTRUCCIONES:
    1. Copia este archivo como 'config.py'
    2. Completa los valores con tu información real
    3. Asegúrate de que config.py esté en .gitignore
    """
    
    # Configuración de la base de datos SQL Server
    # Reemplaza con los datos de tu servidor SQL Server
    DB_SERVER = 'tu-servidor-sql.ejemplo.com'
    DB_NAME = 'nombre_de_tu_base_de_datos'
    DB_USER = 'tu_usuario_sql'
    DB_PASSWORD = 'tu_contraseña_sql'
    
    # Configuración de Flask
    # Genera una clave secreta segura para producción
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cambia-esta-clave-secreta-en-produccion'
    DEBUG = True  # Cambia a False en producción
    
    # Configuración de búsqueda
    # Número de días por defecto para búsquedas
    DEFAULT_SEARCH_DAYS = 365
    
    # Configuración adicional (opcional)
    # Puedes agregar más configuraciones según tus necesidades
    # TIMEOUT_CONEXION = 30
    # MAX_RESULTADOS = 1000