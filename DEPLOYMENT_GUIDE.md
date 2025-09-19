# Guía de Despliegue - Módulo de Búsqueda de Datos de Pasajeros



## Requisitos Previos

### 1. Python 3.8 o superior
```powershell
# Verificar versión de Python
python --version

# Si no está instalado, descargar desde:
# https://www.python.org/downloads/
```

### 2. Configuración de Red
- Asegurar que el puerto 5000 esté abierto en el firewall
- Verificar conectividad de red desde otras computadoras

## Pasos de Instalación

### Paso 1: Preparar el Directorio
```powershell
# Crear directorio para la aplicación
mkdir C:\Apps\BuscaDatosPasajero
cd C:\Apps\BuscaDatosPasajero
```

### Paso 2: Copiar Archivos
Copiar todos los archivos del proyecto al servidor:
- `app.py`
- `config.py`
- `requirements.txt`
- `README.md`
- `templates/index.html`
- `deploy_server.py` (archivo de producción)
- `install_dependencies.bat`

### Paso 3: Crear Entorno Virtual
```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate
```

### Paso 4: Instalar Dependencias
```powershell
# Instalar dependencias
pip install -r requirements.txt

# Instalar servidor WSGI para producción
pip install waitress
```

### Paso 5: Configurar Base de Datos
Editar `config.py` con las credenciales correctas:
```python
# Configuración de base de datos
DATABASE_CONFIG = {
    'server': '',
    'database': '',
    'username': '',
    'password': ''
}
```

### Paso 6: Configurar para Producción
Crear archivo `deploy_server.py` para servidor de producción.

## Configuración de Firewall

### Windows Firewall
```powershell
# Abrir puerto 5000 en firewall (ejecutar como administrador)
netsh advfirewall firewall add rule name="Flask App Port 5000" dir=in action=allow protocol=TCP localport=5000
```

## Ejecución en Producción

### Opción 1: Servidor de Desarrollo (para pruebas)
```powershell
cd C:\Apps\BuscaDatosPasajero
venv\Scripts\activate
python app.py
```

### Opción 2: Servidor de Producción (recomendado)
```powershell
cd C:\Apps\BuscaDatosPasajero
venv\Scripts\activate
python deploy_server.py
```

## Acceso desde Otras Computadoras

Una vez desplegado, la aplicación estará disponible en:
- **URL Local**: http://localhost:5000
- **URL de Red**: http://IP:5000

### Desde otras computadoras en la red:
```
http://IP:5000
```

## Configuración como Servicio de Windows

Para que la aplicación se ejecute automáticamente:

### 1. Instalar NSSM (Non-Sucking Service Manager)
- Descargar desde: https://nssm.cc/download
- Extraer a `C:\nssm`

### 2. Crear el servicio
```powershell
# Ejecutar como administrador
C:\nssm\win64\nssm.exe install "BuscaDatosPasajero"

# Configurar:
# Path: C:\Apps\BuscaDatosPasajero\venv\Scripts\python.exe
# Startup directory: C:\Apps\BuscaDatosPasajero
# Arguments: deploy_server.py
```

### 3. Iniciar el servicio
```powershell
net start BuscaDatosPasajero
```

## Monitoreo y Logs

### Verificar estado del servicio
```powershell
# Ver servicios en ejecución
Get-Service | Where-Object {$_.Name -like "*BuscaDatos*"}

# Ver logs del sistema
Get-EventLog -LogName Application -Source "BuscaDatosPasajero" -Newest 10
```

### Verificar conectividad
```powershell
# Desde otra computadora, probar conectividad
Test-NetConnection -ComputerName IP -Port 5000
```

## Solución de Problemas

### Problema: No se puede acceder desde otras computadoras
**Solución**:
1. Verificar firewall de Windows
2. Comprobar que Flask esté configurado para escuchar en todas las interfaces (0.0.0.0)
3. Verificar conectividad de red

### Problema: Error de conexión a base de datos
**Solución**:
1. Verificar credenciales en `config.py`
2. Comprobar conectividad al servidor SQL (IP Server)
3. Verificar que el driver ODBC esté instalado

### Problema: Aplicación lenta
**Solución**:
1. Verificar índices en la tabla TCDOCU_CLIE
2. Monitorear uso de CPU y memoria
3. Considerar optimizaciones adicionales en consultas SQL

## Mantenimiento

### Actualización de la aplicación
1. Detener el servicio
2. Hacer backup de archivos actuales
3. Copiar nuevos archivos
4. Reiniciar el servicio

### Backup de configuración
```powershell
# Crear backup de configuración
copy C:\Apps\BuscaDatosPasajero\config.py C:\Backup\config_backup.py
```

## Contacto y Soporte

Para soporte técnico o problemas de despliegue, contactar al administrador del sistema.

---
**Nota**: Esta guía asume que el servidor de base de datos () es accesible desde el servidor de aplicaciones ().