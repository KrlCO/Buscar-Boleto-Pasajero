@echo off
setlocal enabledelayedexpansion

echo ========================================
echo CORRECCION DE RUTAS EN WEB.CONFIG
echo Solucion para error 0x8007010b
echo ========================================
echo.

set TIMESTAMP=%date:~-4,4%-%date:~-10,2%-%date:~-7,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%
set TIMESTAMP=!TIMESTAMP: =0!

echo [1/8] Verificando permisos de administrador...
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo     ❌ ERROR: Se requieren permisos de administrador
    echo     Ejecute este script como administrador
    pause
    exit /b 1
)
echo     ✓ Permisos de administrador verificados

echo.
echo [2/8] Creando backup del web.config actual...
if exist "web.config" (
    copy "web.config" "web.config.backup.%TIMESTAMP%" >nul 2>&1
    echo     ✓ Backup creado: web.config.backup.%TIMESTAMP%
) else (
    echo     ❌ ERROR: web.config no encontrado
    goto :error
)

echo.
echo [3/8] Detectando ruta de Python en el servidor...
echo     Buscando Python en ubicaciones comunes...
set PYTHON_FOUND=0
set PYTHON_PATH=
set WFASTCGI_PATH=

REM Buscar Python en ubicaciones comunes del servidor
for %%p in (
    "C:\Python313\python.exe"
    "C:\Python312\python.exe"
    "C:\Python311\python.exe"
    "C:\Python310\python.exe"
    "C:\Program Files\Python313\python.exe"
    "C:\Program Files\Python312\python.exe"
    "C:\Program Files\Python311\python.exe"
    "C:\Program Files\Python310\python.exe"
    "C:\Program Files (x86)\Python313\python.exe"
    "C:\Program Files (x86)\Python312\python.exe"
    "C:\Program Files (x86)\Python311\python.exe"
    "C:\Program Files (x86)\Python310\python.exe"
) do (
    if exist %%p (
        set PYTHON_PATH=%%~p
        set PYTHON_FOUND=1
        echo     ✓ Python encontrado en: %%~p
        goto :python_found
    )
)

REM Si no se encuentra, usar el comando where
for /f "tokens=*" %%i in ('where python 2^>nul') do (
    set PYTHON_PATH=%%i
    set PYTHON_FOUND=1
    echo     ✓ Python encontrado en PATH: %%i
    goto :python_found
)

if %PYTHON_FOUND%==0 (
    echo     ❌ ERROR: Python no encontrado en el servidor
    goto :error
)

:python_found
echo.
echo [4/8] Verificando wfastcgi...
echo     Verificando instalacion de wfastcgi...

REM Obtener directorio de Python
for %%i in ("%PYTHON_PATH%") do set PYTHON_DIR=%%~dpi
set PYTHON_DIR=%PYTHON_DIR:~0,-1%

REM Buscar wfastcgi.py
set WFASTCGI_FOUND=0
for %%w in (
    "%PYTHON_DIR%\Lib\site-packages\wfastcgi.py"
    "%PYTHON_DIR%\lib\site-packages\wfastcgi.py"
    "%PYTHON_DIR%\Scripts\wfastcgi.py"
) do (
    if exist %%w (
        set WFASTCGI_PATH=%%~w
        set WFASTCGI_FOUND=1
        echo     ✓ wfastcgi encontrado en: %%~w
        goto :wfastcgi_found
    )
)

if %WFASTCGI_FOUND%==0 (
    echo     ⚠️  wfastcgi no encontrado, instalando...
    "%PYTHON_PATH%" -m pip install wfastcgi
    if !errorLevel! neq 0 (
        echo     ❌ ERROR: No se pudo instalar wfastcgi
        goto :error
    )
    
    REM Buscar nuevamente
    for %%w in (
        "%PYTHON_DIR%\Lib\site-packages\wfastcgi.py"
        "%PYTHON_DIR%\lib\site-packages\wfastcgi.py"
    ) do (
        if exist %%w (
            set WFASTCGI_PATH=%%~w
            set WFASTCGI_FOUND=1
            echo     ✓ wfastcgi instalado en: %%~w
            goto :wfastcgi_found
        )
    )
)

if %WFASTCGI_FOUND%==0 (
    echo     ❌ ERROR: No se pudo encontrar wfastcgi despues de la instalacion
    goto :error
)

:wfastcgi_found
echo.
echo [5/8] Generando nuevo web.config con rutas correctas...
echo     Python: %PYTHON_PATH%
echo     wfastcgi: %WFASTCGI_PATH%
echo     Directorio actual: %CD%

(
    echo ^<?xml version="1.0" encoding="utf-8"?^>
    echo ^<configuration^>
    echo   ^<system.webServer^>
    echo     ^<handlers^>
    echo       ^<clear /^>
    echo       ^<add name="Python FastCGI"
    echo            path="*"
    echo            verb="*"
    echo            modules="FastCgiModule"
    echo            scriptProcessor="%PYTHON_PATH%^|%WFASTCGI_PATH%"
    echo            resourceType="Unspecified"
    echo            requireAccess="Script" /^>
    echo     ^</handlers^>
    echo     ^<defaultDocument^>
    echo       ^<files^>
    echo         ^<clear /^>
    echo         ^<add value="app_iis.py" /^>
    echo       ^</files^>
    echo     ^</defaultDocument^>
    echo     ^<httpErrors errorMode="Detailed" /^>
    echo     ^<security^>
    echo       ^<requestFiltering^>
    echo         ^<hiddenSegments^>
    echo           ^<add segment=".venv" /^>
    echo           ^<add segment="venv" /^>
    echo           ^<add segment="__pycache__" /^>
    echo         ^</hiddenSegments^>
    echo       ^</requestFiltering^>
    echo     ^</security^>
    echo   ^</system.webServer^>
    echo   ^<appSettings^>
    echo     ^<add key="WSGI_HANDLER" value="app_iis.application" /^>
    echo     ^<add key="PYTHONPATH" value="%CD%" /^>
    echo     ^<add key="WSGI_LOG" value="%CD%\logs\wsgi.log" /^>
    echo     ^<add key="WSGI_RESTART_FILE_REGEX" value=".*^^(app_iis^|app^|config^^)\.py$" /^>
    echo   ^</appSettings^>
    echo ^</configuration^>
) > "web.config"
echo     ✓ Nuevo web.config generado

echo.
echo [6/8] Configurando FastCGI en IIS...
echo     Eliminando configuracion FastCGI anterior...
%windir%\system32\inetsrv\appcmd.exe clear config -section:system.webServer/fastCgi >nul 2>&1

echo     Configurando nueva aplicacion FastCGI...
%windir%\system32\inetsrv\appcmd.exe set config -section:system.webServer/fastCgi /+[fullPath='%PYTHON_PATH%',arguments='%WFASTCGI_PATH%',maxInstances='4',idleTimeout='1800',activityTimeout='30',requestTimeout='90',instanceMaxRequests='1000',protocol='NamedPipe',flushNamedPipe='False'] /commit:apphost
if %errorLevel% neq 0 (
    echo     ❌ ERROR: No se pudo configurar FastCGI
    goto :error
)
echo     ✓ FastCGI configurado correctamente

echo.
echo [7/8] Verificando y creando directorio de logs...
if not exist "logs" (
    mkdir "logs"
    echo     ✓ Directorio logs creado
) else (
    echo     ✓ Directorio logs existe
)

echo     Configurando permisos para logs...
icacls "logs" /grant "IIS_IUSRS:(OI)(CI)F" >nul 2>&1
icacls "logs" /grant "IUSR:(OI)(CI)F" >nul 2>&1
echo     ✓ Permisos de logs configurados

echo.
echo [8/8] Reiniciando IIS...
echo     Reciclando Application Pool...
%windir%\system32\inetsrv\appcmd.exe recycle apppool "BuscaDatosPasajero" >nul 2>&1

echo     Reiniciando sitio web...
%windir%\system32\inetsrv\appcmd.exe stop site "BuscaDatosPasajero" >nul 2>&1
timeout /t 2 /nobreak >nul
%windir%\system32\inetsrv\appcmd.exe start site "BuscaDatosPasajero" >nul 2>&1
echo     ✓ IIS reiniciado

echo.
echo ========================================
echo CORRECCION COMPLETADA
echo ========================================
echo.
echo 🎯 Cambios realizados:
echo ✓ Rutas de Python corregidas en web.config
echo ✓ Ruta de wfastcgi corregida
echo ✓ PYTHONPATH actualizado al directorio actual
echo ✓ Directorio de logs configurado
echo ✓ FastCGI reconfigurado en IIS
echo ✓ Permisos de logs establecidos
echo ✓ IIS reiniciado
echo.
echo 📋 Configuracion aplicada:
echo - Python: %PYTHON_PATH%
echo - wfastcgi: %WFASTCGI_PATH%
echo - Directorio: %CD%
echo - Logs: %CD%\logs
echo.
echo 🌐 Probar la aplicacion en:
echo http://10.10.10.32:9547/
echo.
echo 📊 Si el error persiste:
echo 1. Verificar que app_iis.py funcione: python app_iis.py
echo 2. Revisar logs en: %CD%\logs\wsgi.log
echo 3. Ejecutar: analyze_0x8007010b_remote.bat
echo.
echo ========================================
goto :end

:error
echo.
echo ❌ ERROR: No se pudo completar la correccion
echo.
echo 🔧 Verificaciones manuales:
echo 1. Confirmar que Python este instalado en el servidor
echo 2. Verificar que wfastcgi este instalado
echo 3. Ejecutar como administrador
echo 4. Revisar permisos de archivos
echo.
echo 📞 Informacion para soporte:
echo - Error: 0x8007010b - Rutas incorrectas en web.config
echo - Timestamp: %TIMESTAMP%
echo - Python detectado: %PYTHON_PATH%
echo - wfastcgi detectado: %WFASTCGI_PATH%
echo.

:end
echo.
pause