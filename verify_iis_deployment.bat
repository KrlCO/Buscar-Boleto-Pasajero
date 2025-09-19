@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Verificacion de Despliegue en IIS
echo Servidor: [CONFIGURAR_IP_SERVIDOR]
echo ========================================
echo.

set APP_DIR=C:\inetpub\wwwroot\BuscaDatosPasajero
set SERVER_IP=[CONFIGURAR_IP_SERVIDOR]
set APP_PORT=9547

echo [1/7] Verificando archivos de aplicacion...
if not exist "%APP_DIR%\app.py" (
    echo     ❌ ERROR: app.py no encontrado
    goto :error
)
if not exist "%APP_DIR%\app_iis.py" (
    echo     ❌ ERROR: app_iis.py no encontrado
    goto :error
)
if not exist "%APP_DIR%\web.config" (
    echo     ❌ ERROR: web.config no encontrado
    goto :error
)
if not exist "%APP_DIR%\config.py" (
    echo     ❌ ERROR: config.py no encontrado
    goto :error
)
echo     ✓ Todos los archivos principales presentes

echo.
echo [2/7] Verificando dependencias Python...
cd /d "%APP_DIR%"
python -c "import flask; print('Flask version:', flask.__version__)" >nul 2>&1
if %errorLevel% neq 0 (
    echo     ❌ ERROR: Flask no instalado
    goto :error
)

python -c "import pyodbc; print('pyodbc OK')" >nul 2>&1
if %errorLevel% neq 0 (
    echo     ❌ ERROR: pyodbc no instalado
    goto :error
)

python -c "import wfastcgi; print('wfastcgi OK')" >nul 2>&1
if %errorLevel% neq 0 (
    echo     ❌ ERROR: wfastcgi no instalado
    goto :error
)
echo     ✓ Dependencias Python OK

echo.
echo [3/7] Verificando configuracion de IIS...
%windir%\system32\inetsrv\appcmd.exe list sites | findstr "BuscaDatosPasajero" >nul 2>&1
if %errorLevel% neq 0 (
    echo     ⚠️  ADVERTENCIA: Sitio 'BuscaDatosPasajero' no encontrado en IIS
    echo     Debe crear el sitio manualmente en IIS Manager
) else (
    echo     ✓ Sitio encontrado en IIS
)

%windir%\system32\inetsrv\appcmd.exe list apppools | findstr "BuscaDatosPasajeroPool" >nul 2>&1
if %errorLevel% neq 0 (
    echo     ⚠️  ADVERTENCIA: Application Pool 'BuscaDatosPasajeroPool' no encontrado
    echo     Debe crear el Application Pool manualmente
) else (
    echo     ✓ Application Pool encontrado
)

echo.
echo [4/7] Verificando permisos de archivos...
icacls "%APP_DIR%" | findstr "IIS_IUSRS" >nul 2>&1
if %errorLevel% neq 0 (
    echo     ❌ ERROR: Permisos IIS_IUSRS no configurados
    goto :error
)
echo     ✓ Permisos IIS configurados

echo.
echo [5/7] Verificando logs...
if not exist "%APP_DIR%\logs" (
    mkdir "%APP_DIR%\logs"
    echo     ✓ Directorio de logs creado
) else (
    echo     ✓ Directorio de logs existe
)

echo.
echo [6/7] Probando importacion de aplicacion...
python -c "import sys; sys.path.insert(0, '.'); from app_iis import application; print('Aplicacion cargada exitosamente')" 2>temp_error.txt
if %errorLevel% neq 0 (
    echo     ❌ ERROR: No se puede cargar la aplicacion
    echo     Detalles del error:
    type temp_error.txt
    del temp_error.txt
    goto :error
)
if exist temp_error.txt del temp_error.txt
echo     ✓ Aplicacion se carga correctamente

echo.
echo [7/7] Verificando conectividad de red...
ping -n 1 %SERVER_IP% >nul 2>&1
if %errorLevel% neq 0 (
    echo     ❌ ERROR: No se puede hacer ping a %SERVER_IP%
    goto :error
)
echo     ✓ Conectividad de red OK

echo.
echo ========================================
echo VERIFICACION COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo Estado del despliegue:
echo ✓ Archivos de aplicacion: OK
echo ✓ Dependencias Python: OK
echo ✓ Permisos IIS: OK
echo ✓ Aplicacion Flask: OK
echo ✓ Conectividad: OK
echo.
echo Proximos pasos:
echo 1. Configurar sitio en IIS Manager (si no esta hecho)
echo 2. Configurar config.py con datos de base de datos
echo 3. Probar acceso:
echo    - Local: http://localhost:%APP_PORT%
echo    - Red: http://%SERVER_IP%:%APP_PORT%
echo.
echo URLs de prueba:
echo curl http://localhost:%APP_PORT%
echo curl http://%SERVER_IP%:%APP_PORT%
echo.
echo ========================================
echo Aplicacion lista para produccion
echo ========================================
goto :end

:error
echo.
echo ========================================
echo ERROR EN LA VERIFICACION
echo ========================================
echo.
echo Revise los errores anteriores y corrija antes de continuar.
echo Consulte la documentacion en DEPLOYMENT_IIS_GUIDE.md
echo.
echo Comandos utiles para diagnostico:
echo - Verificar IIS: %%windir%%\system32\inetsrv\appcmd.exe list sites
echo - Verificar Python: python --version
echo - Verificar dependencias: pip list
echo - Verificar logs: type "%APP_DIR%\logs\*.log"
echo.

:end
echo.
pause