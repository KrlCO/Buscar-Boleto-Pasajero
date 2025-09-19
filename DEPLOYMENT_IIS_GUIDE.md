# Guía de Despliegue en IIS - Módulo de Búsqueda de Datos de Pasajeros

## 🌐 Despliegue en IIS (Recomendado)

### Ventajas de usar IIS
- ✅ **Infraestructura existente**: Aprovecha IIS ya configurado
- ✅ **Mejor rendimiento**: IIS optimizado para Windows Server
- ✅ **Gestión centralizada**: Junto con otros proyectos existentes
- ✅ **Seguridad robusta**: Configuración de seguridad empresarial
- ✅ **Logs integrados**: Sistema de logs unificado
- ✅ **SSL/HTTPS**: Fácil configuración de certificados


## 🚀 Instalación en IIS

### Paso 1: Preparar el Entorno Python

```cmd
# 1. Crear directorio en IIS
mkdir C:\inetpub\wwwroot\BuscaDatosPasajero
cd C:\inetpub\wwwroot\BuscaDatosPasajero

# 2. Copiar archivos del proyecto
# Copiar todos los archivos desde d:\PROJECTS\BuscaDatosPasajero
```

### Paso 2: Instalar wfastcgi

```cmd
# Instalar wfastcgi para IIS
pip install wfastcgi

# Habilitar wfastcgi en IIS
wfastcgi-enable
```

### Paso 3: Configurar web.config

Crear `C:\inetpub\wwwroot\BuscaDatosPasajero\web.config`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="Python FastCGI" 
           path="*" 
           verb="*" 
           modules="FastCgiModule" 
           scriptProcessor="C:\Python\python.exe|C:\Python\Lib\site-packages\wfastcgi.py" 
           resourceType="Unspecified" 
           requireAccess="Script" />
    </handlers>
    <defaultDocument>
      <files>
        <clear />
        <add value="app.py" />
      </files>
    </defaultDocument>
  </system.webServer>
  <appSettings>
    <add key="WSGI_HANDLER" value="app.app" />
    <add key="PYTHONPATH" value="C:\inetpub\wwwroot\BuscaDatosPasajero" />
    <add key="WSGI_LOG" value="C:\inetpub\wwwroot\BuscaDatosPasajero\logs\app.log" />
  </appSettings>
</configuration>
```

### Paso 4: Crear Sitio en IIS

1. **Abrir IIS Manager**
2. **Crear nuevo sitio**:
   - Nombre: `BuscaDatosPasajero`
   - Ruta física: `C:\inetpub\wwwroot\BuscaDatosPasajero`
   - Puerto: `9547` (puerto poco común para evitar conflictos)
   - IP: ``

3. **Configurar Application Pool**:
   - Nombre: `BuscaDatosPasajeroPool`
   - .NET Framework: `No Managed Code`
   - Modo: `Integrated`

### Paso 5: Configurar Permisos

```cmd
# Dar permisos al usuario IIS
icacls "C:\inetpub\wwwroot\BuscaDatosPasajero" /grant "IIS_IUSRS:(OI)(CI)F" /T
icacls "C:\inetpub\wwwroot\BuscaDatosPasajero" /grant "IUSR:(OI)(CI)F" /T
```

## 🔧 Configuración Específica para Flask

### Modificar app.py para IIS

Crear `app_iis.py`:

```python
import os
import sys

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

# Importar la aplicación Flask
from app import app

# Configuración para IIS
if __name__ == '__main__':
    app.run(debug=False)
```

### Actualizar web.config

```xml
<appSettings>
    <add key="WSGI_HANDLER" value="app_iis.app" />
    <add key="PYTHONPATH" value="C:\inetpub\wwwroot\BuscaDatosPasajero" />
    <add key="WSGI_LOG" value="C:\inetpub\wwwroot\BuscaDatosPasajero\logs\app.log" />
</appSettings>
```

## 🌐 Acceso a la Aplicación

### URLs de Acceso
- **Local**: http://localhost:9547
- **Red**: http://:9547
- **Con dominio**: http://servidor.empresa.com:9547 (si está configurado)

## 📊 Ventajas del Despliegue en IIS

### Rendimiento
- **Mejor gestión de memoria**: IIS optimiza el uso de RAM
- **Balanceador de carga**: Distribución automática de requests
- **Compresión**: Compresión automática de respuestas
- **Caché**: Sistema de caché integrado

### Administración
- **Logs centralizados**: Junto con otros sitios web
- **Monitoreo**: Herramientas de monitoreo integradas
- **Backup**: Políticas de backup existentes
- **Seguridad**: Configuración de seguridad empresarial

### Escalabilidad
- **Múltiples workers**: Procesos paralelos automáticos
- **Reinicio automático**: En caso de errores
- **Gestión de recursos**: Límites de CPU y memoria

## 🔒 Configuración de Seguridad

### SSL/HTTPS (Recomendado)

1. **Instalar certificado SSL** en IIS
2. **Configurar binding HTTPS**:
   - Puerto: 443
   - Certificado: Seleccionar certificado instalado

3. **Forzar HTTPS**:
```xml
<system.webServer>
    <rewrite>
        <rules>
            <rule name="Redirect to HTTPS" stopProcessing="true">
                <match url="(.*)" />
                <conditions>
                    <add input="{HTTPS}" pattern="off" ignoreCase="true" />
                </conditions>
                <action type="Redirect" url="https://{HTTP_HOST}/{R:1}" redirectType="Permanent" />
            </rule>
        </rules>
    </rewrite>
</system.webServer>
```

## 🛠️ Script de Instalación Automática

Crear `deploy_to_iis.bat`:

```batch
@echo off
echo ========================================
echo Desplegando en IIS - Busca Datos Pasajero
echo ========================================

# Crear directorio
mkdir C:\inetpub\wwwroot\BuscaDatosPasajero

# Copiar archivos
xcopy /E /I /Y "d:\PROJECTS\BuscaDatosPasajero\*" "C:\inetpub\wwwroot\BuscaDatosPasajero\"

# Instalar dependencias
cd C:\inetpub\wwwroot\BuscaDatosPasajero
pip install -r requirements.txt
pip install wfastcgi

# Habilitar FastCGI
wfastcgi-enable

# Configurar permisos
icacls "C:\inetpub\wwwroot\BuscaDatosPasajero" /grant "IIS_IUSRS:(OI)(CI)F" /T

echo ========================================
echo Despliegue completado
echo ========================================
echo.
echo Pasos restantes:
echo 1. Crear sitio en IIS Manager
echo 2. Configurar Application Pool
echo 3. Probar acceso: http://:9547
echo.
pause
```

## 🔍 Troubleshooting

### Problemas Comunes

1. **Error 500**: Verificar logs en `C:\inetpub\wwwroot\BuscaDatosPasajero\logs\`
2. **Módulo no encontrado**: Verificar PYTHONPATH en web.config
3. **Permisos**: Verificar permisos de IIS_IUSRS
4. **Base de datos**: Verificar conectividad desde el servidor IIS

### Logs

- **IIS Logs**: `C:\inetpub\logs\LogFiles\`
- **Application Logs**: `C:\inetpub\wwwroot\BuscaDatosPasajero\logs\`
- **Event Viewer**: Windows Logs > Application

## 📈 Monitoreo y Mantenimiento

### Métricas a Monitorear
- **CPU Usage**: Application Pool
- **Memory Usage**: Proceso Python
- **Response Time**: Tiempo de respuesta
- **Error Rate**: Errores 500/404

### Mantenimiento
- **Logs**: Limpiar logs antiguos semanalmente
- **Updates**: Actualizar dependencias mensualmente
- **Backup**: Backup del directorio de aplicación
- **Monitoring**: Configurar alertas en IIS

---

## ✅ Resumen

**IIS es la mejor opción** para este servidor porque:
- Aprovecha la infraestructura existente
- Mejor rendimiento y estabilidad
- Gestión centralizada con otros proyectos
- Configuración de seguridad empresarial
- Escalabilidad automática

**URL Final**: http://:9547 (o HTTPS si se configura SSL)

---

**Nota**: Esta configuración aprovecha IIS existente y proporciona mejor rendimiento que el servidor Flask standalone.