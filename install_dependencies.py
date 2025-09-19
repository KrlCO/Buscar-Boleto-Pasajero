#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de instalación de dependencias para BuscaDatosPasajero
Instala todas las dependencias necesarias incluyendo herramientas de compilación
para evitar problemas con las 'ruedas' en diferentes versiones de Python.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    print(f"Ejecutando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print("✅ Éxito!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print(f"Salida: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Verifica la versión de Python"""
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("⚠️  Advertencia: Se recomienda Python 3.8 o superior")
        return False
    return True

def upgrade_pip():
    """Actualiza pip a la última versión"""
    return run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Actualizando pip a la última versión"
    )

def install_build_tools():
    """Instala herramientas de compilación básicas"""
    build_tools = [
        "setuptools",
        "wheel", 
        "cython",
        "numpy"
    ]
    
    command = f"{sys.executable} -m pip install {' '.join(build_tools)}"
    return run_command(
        command,
        "Instalando herramientas de compilación (setuptools, wheel, cython, numpy)"
    )

def install_requirements():
    """Instala dependencias desde requirements.txt"""
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(f"❌ Error: No se encontró el archivo {requirements_file}")
        return False
    
    command = f"{sys.executable} -m pip install -r {requirements_file}"
    return run_command(
        command,
        "Instalando dependencias desde requirements.txt"
    )

def verify_installation():
    """Verifica que las dependencias principales estén instaladas"""
    print(f"\n{'='*60}")
    print("🔍 Verificando instalación")
    print(f"{'='*60}")
    
    required_packages = [
        "flask",
        "pyodbc", 
        "werkzeug",
        "jinja2",
        "waitress",
        "wfastcgi"
    ]
    
    all_installed = True
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}: Instalado")
        except ImportError:
            print(f"❌ {package}: NO instalado")
            all_installed = False
    
    return all_installed

def main():
    """Función principal"""
    print("🚀 Instalador de Dependencias - BuscaDatosPasajero")
    print("=" * 60)
    
    # Verificar versión de Python
    if not check_python_version():
        print("⚠️  Continuando con la versión actual de Python...")
    
    success_count = 0
    total_steps = 4
    
    # Paso 1: Actualizar pip
    if upgrade_pip():
        success_count += 1
    
    # Paso 2: Instalar herramientas de compilación
    if install_build_tools():
        success_count += 1
    
    # Paso 3: Instalar dependencias
    if install_requirements():
        success_count += 1
    
    # Paso 4: Verificar instalación
    if verify_installation():
        success_count += 1
    
    # Resumen final
    print(f"\n{'='*60}")
    print("📊 RESUMEN DE INSTALACIÓN")
    print(f"{'='*60}")
    print(f"Pasos completados: {success_count}/{total_steps}")
    
    if success_count == total_steps:
        print("🎉 ¡Instalación completada exitosamente!")
        print("\n📋 Próximos pasos:")
        print("   1. Ejecutar: python app.py")
        print("   2. Abrir navegador en: http://127.0.0.1:5000")
        return True
    else:
        print("⚠️  Instalación completada con algunos errores")
        print("\n🔧 Soluciones sugeridas:")
        print("   1. Ejecutar como administrador")
        print("   2. Verificar conexión a internet")
        print("   3. Actualizar Python a una versión más reciente")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Instalación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Error inesperado: {e}")
        sys.exit(1)