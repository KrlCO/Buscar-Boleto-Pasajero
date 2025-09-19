@echo off
REM Script de inicio simple para la aplicación de Búsqueda de Datos de Pasajeros

echo ========================================
echo  INICIANDO APLICACION
echo ========================================
echo.

REM Verificar si existe el entorno virtual
if not exist ".venv" (
    echo ERROR: Entorno virtual .venv no encontrado
    echo.
    echo Por favor ejecute: python -m venv .venv
    echo Luego instale dependencias: .venv\Scripts\pip install flask pyodbc
    echo.
    pause
    exit /b 1
)

REM Activar entorno virtual y ejecutar aplicación
echo Activando entorno virtual...
call .venv\Scripts\activate.bat

echo Iniciando servidor Flask...
echo.
echo La aplicación estará disponible en:
echo   http://localhost:5000
echo   http://127.0.0.1:5000
echo.
echo Presione Ctrl+C para detener el servidor
echo.

REM Ejecutar la aplicación
python app.py

echo.
echo Aplicación detenida.
pause