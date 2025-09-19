@echo off
REM Script de instalación de dependencias para BuscaDatosPasajero
REM Ejecuta el instalador de Python con manejo de errores

echo ========================================
echo  Instalador de Dependencias
echo  BuscaDatosPasajero
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado o no está en el PATH
    echo.
    echo 📋 Soluciones:
    echo    1. Instalar Python desde https://python.org
    echo    2. Agregar Python al PATH del sistema
    echo    3. Reiniciar el terminal después de la instalación
    pause
    exit /b 1
)

echo ✅ Python encontrado:
python --version
echo.

REM Verificar si pip está disponible
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: pip no está disponible
    echo.
    echo 📋 Solución:
    echo    Reinstalar Python con la opción "Add Python to PATH"
    pause
    exit /b 1
)

echo ✅ pip encontrado:
python -m pip --version
echo.

REM Ejecutar el script de instalación de Python
echo 🚀 Iniciando instalación de dependencias...
echo.

python install_dependencies.py

REM Verificar el resultado
if errorlevel 1 (
    echo.
    echo ❌ La instalación falló con errores
    echo.
    echo 🔧 Soluciones sugeridas:
    echo    1. Ejecutar como administrador
    echo    2. Verificar conexión a internet
    echo    3. Actualizar Python a una versión más reciente
    echo    4. Revisar los mensajes de error anteriores
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo 🎉 ¡Instalación completada exitosamente!
    echo.
    echo 📋 Para iniciar la aplicación:
    echo    1. Ejecutar: python app.py
    echo    2. Abrir navegador en: http://127.0.0.1:5000
    echo.
    echo ¿Desea iniciar la aplicación ahora? (S/N)
    set /p choice="Respuesta: "
    if /i "%choice%"=="S" (
        echo.
        echo 🚀 Iniciando aplicación...
        python app.py
    ) else (
        echo.
        echo 👍 Puede iniciar la aplicación manualmente cuando esté listo
    )
)

echo.
echo Presione cualquier tecla para salir...
pause >nul