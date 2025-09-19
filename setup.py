#!/usr/bin/env python3
"""
Script de configuración automática para Buscar Boleto Pasajero
Este script ayuda a configurar el proyecto para nuevos usuarios
"""

import os
import shutil
import sys
from pathlib import Path

def print_banner():
    """Muestra el banner de bienvenida"""
    print("=" * 60)
    print("🚌 CONFIGURACIÓN DE BUSCAR BOLETO PASAJERO")
    print("=" * 60)
    print()

def check_python_version():
    """Verifica que la versión de Python sea compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Se requiere Python 3.7 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    print(f"✓ Python {sys.version.split()[0]} detectado")
    return True

def create_config_files():
    """Crea los archivos de configuración si no existen"""
    print("\n📁 Creando archivos de configuración...")
    
    # Crear config.py desde config.example.py
    if not os.path.exists('config.py'):
        if os.path.exists('config.example.py'):
            shutil.copy('config.example.py', 'config.py')
            print("✓ config.py creado desde config.example.py")
        else:
            print("❌ No se encontró config.example.py")
            return False
    else:
        print("ℹ️  config.py ya existe")
    
    # Crear .env desde .env.example
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            shutil.copy('.env.example', '.env')
            print("✓ .env creado desde .env.example")
        else:
            print("❌ No se encontró .env.example")
            return False
    else:
        print("ℹ️  .env ya existe")
    
    # Crear web.config desde web.config.example (si existe)
    if os.path.exists('web.config.example') and not os.path.exists('web.config'):
        shutil.copy('web.config.example', 'web.config')
        print("✓ web.config creado desde web.config.example")
    
    return True

def install_dependencies():
    """Instala las dependencias del proyecto"""
    print("\n📦 Instalando dependencias...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Dependencias instaladas correctamente")
            return True
        else:
            print(f"❌ Error instalando dependencias: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando pip: {e}")
        return False

def show_next_steps():
    """Muestra los siguientes pasos para el usuario"""
    print("\n🎉 ¡Configuración inicial completada!")
    print("\n📋 SIGUIENTES PASOS:")
    print("1. Edita el archivo .env con tu configuración de base de datos:")
    print("   - DB_SERVER: Tu servidor SQL Server")
    print("   - DB_NAME: Nombre de tu base de datos")
    print("   - DB_USER: Usuario de la base de datos")
    print("   - DB_PASSWORD: Contraseña de la base de datos")
    print()
    print("2. Si usas IIS, edita web.config con las rutas correctas")
    print()
    print("3. Ejecuta la aplicación:")
    print("   python app.py")
    print()
    print("4. Para más información, consulta README.md")
    print()
    print("⚠️  IMPORTANTE: Nunca subas config.py, .env o web.config a GitHub")
    print("   Estos archivos están en .gitignore por seguridad")

def main():
    """Función principal del script de configuración"""
    print_banner()
    
    # Verificar versión de Python
    if not check_python_version():
        sys.exit(1)
    
    # Crear archivos de configuración
    if not create_config_files():
        print("\n❌ Error creando archivos de configuración")
        sys.exit(1)
    
    # Instalar dependencias
    if not install_dependencies():
        print("\n❌ Error instalando dependencias")
        print("💡 Intenta ejecutar manualmente: pip install -r requirements.txt")
        sys.exit(1)
    
    # Mostrar siguientes pasos
    show_next_steps()

if __name__ == "__main__":
    main()