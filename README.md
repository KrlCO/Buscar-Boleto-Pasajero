# Módulo de Búsqueda de Datos de Pasajeros

Aplicación web desarrollada en Python + Flask para buscar datos de pasajeros en la base de datos SQL Server.

## Características

- **Búsqueda por código de cliente (CO_CLIE)**: Parámetro principal requerido
- **Filtros avanzados**: Búsqueda por DNI, tipo de documento y rango de fechas
- **Validación de cliente**: Verifica existencia en tabla TMCLIE
- **Búsqueda principal**: Consulta en tabla TCDOCU_CLIE
- **Interfaz web responsive**: Diseño moderno con Bootstrap 5
- **Persistencia de datos**: Los resultados se guardan automáticamente en localStorage
- **Restauración automática**: Al recargar la página se restauran automáticamente los últimos resultados
- **Gestión de campos**: Botones para limpiar campos y restaurar búsquedas guardadas
- **Resultados detallados**: Muestra todos los campos encontrados en tabla responsive

## Configuración de Base de Datos

- **Servidor**: SALES
- **Base de datos**: VENTas
- **Usuario**: dev08
- **Contraseña**: asdakjdaq


## Instalación de Dependencias

### 🚀 Instalación Rápida para Desarrollo Local

Para instalar todas las dependencias necesarias en su entorno de desarrollo:

```batch
# Ejecutar en el directorio del proyecto
install_dependencies.bat
```

Este script:
- ✅ Verifica la instalación de Python y pip
- 🔧 Instala herramientas de compilación (setuptools, wheel, cython, numpy)
- 📦 Instala todas las dependencias desde requirements.txt
- 🔍 Verifica que todas las dependencias estén correctamente instaladas
- 🚀 Opcionalmente inicia la aplicación

### 📋 Instalación Manual de Dependencias

Si prefiere instalar manualmente:

```bash
# Instalar herramientas de compilación primero
pip install cython numpy setuptools wheel

# Instalar dependencias del proyecto
pip install -r requirements.txt
```

## Despliegue en Servidor

### ⚠️ Si Ya Intentó Configuración Manual

Si ya realizó configuraciones manuales o tiene errores previos, **primero ejecute el script de limpieza**:
```batch
# Ejecutar como administrador - Limpia configuraciones previas
reset_and_cleanup_server_2022.bat
```

### Opción 1: Instalación de Dependencias (Desarrollo Local)
```batch
# Para desarrollo local - Instala todas las dependencias necesarias
install_dependencies.bat
```

### Opción 2: Despliegue Completo en Servidor (Producción)
```batch
# Ejecutar como administrador
deploy_complete_server_2022.bat
```

### Opción 3: Instalación Manual Paso a Paso

1. **Verificar requisitos del servidor**:
   ```batch
   verify_server_2022_requirements.bat
   ```

2. **Instalar Python y dependencias** (IIS ya está configurado):
   ```batch
   install_python_server_2022.bat
   ```

3. **Configurar FastCGI y sitio web**:
   ```batch
   configure_fastcgi_server_2022.bat
   ```

**Nota**: El paso de instalación de IIS se omite ya que el servidor tiene IIS preconfigurado.

### Acceso a la Aplicación
- **URL Local**: http://localhost/
- **URL por IP**: http://[IP_DEL_SERVIDOR]/
- **Logs**: D:\PROJECTS\BuscaDatosPasajero\logs\wfastcgi.log

## Uso

1. **Código de Cliente**: Ingresa el CO_CLIE del pasajero (campo requerido)
2. **Filtros opcionales**: 
   - **DNI**: Número de documento de identidad
   - **Tipo de Documento**: Seleccionar tipo específico
   - **Fechas**: Rango de fechas (formato YYYY-MM-DD)
3. **Hacer clic en "Buscar"**
4. **Ver resultados**:
   - Estado de validación del cliente
   - Parámetros de búsqueda utilizados
   - Tabla responsive con todos los datos encontrados
5. **Funciones adicionales**:
   - **Limpiar Campos**: Borra todos los campos del formulario
   - **Restaurar Búsqueda**: Restaura la última búsqueda guardada
   - **Persistencia automática**: Los resultados se guardan y restauran automáticamente al recargar la página

## Estructura del Proyecto

```
BuscaDatosPasajero/
├── app.py                              # Aplicación principal Flask
├── app_iis.py                          # Aplicación para IIS con wfastcgi
├── config.py                           # Configuración de base de datos
├── requirements.txt                    # Dependencias Python
├── web.config                          # Configuración IIS
├── templates/
│   └── index.html                     # Interfaz web
├── logs/                              # Directorio de logs
│   └── wfastcgi.log                   # Logs de FastCGI
├── Scripts de Instalación de Dependencias:
├── install_dependencies.py            # Instalador inteligente de dependencias
├── install_dependencies.bat           # Script batch para Windows
├── Scripts de Despliegue Windows Server 2022:
├── deploy_complete_server_2022.bat    # Script maestro de despliegue
├── reset_and_cleanup_server_2022.bat  # Limpieza y reset de configuraciones
├── verify_server_2022_requirements.bat # Verificación de requisitos
├── install_iis_server_2022.bat        # Instalación de IIS
├── install_python_server_2022.bat     # Instalación de Python
├── configure_fastcgi_server_2022.bat  # Configuración FastCGI
└── README.md                          # Este archivo
```

## Funcionalidades Técnicas

- **Validación no bloqueante**: Si el cliente no existe en TMCLIE, se muestra advertencia pero continúa la búsqueda
- **Consultas optimizadas**: Uso de WITH(NOLOCK) para mejor rendimiento
- **Manejo robusto de errores**: Prevención de errores NoneType y validación de datos
- **Interfaz moderna**: Bootstrap 5 con diseño responsive y componentes interactivos
- **Persistencia de datos**: localStorage para guardar automáticamente búsquedas y resultados
- **Restauración automática**: Los datos persisten al recargar la página
- **Validación de formularios**: Verificación de campos requeridos y formatos
- **Gestión de estado**: Manejo inteligente de elementos DOM y eventos JavaScript

## Próximas Mejoras

Este es la versión 2.0 con persistencia de datos y funcionalidades avanzadas. Futuras versiones pueden incluir:
- Búsqueda en tablas adicionales
- Exportación de resultados a Excel/PDF
- Autenticación de usuarios
- Logs de auditoría
- Historial de búsquedas
- Filtros adicionales por campos específicos
- API REST para integración con otros sistemas

## Troubleshooting y Comandos Útiles

### Comandos de Administración
```batch
# Reiniciar IIS
iisreset

# Ver estado del sitio web
appcmd list site "Busca Boleto Pasajero"

# Ver configuración FastCGI
appcmd list config /section:system.webServer/fastCGI

# Ver logs de la aplicación
type logs\wfastcgi.log

# Verificar permisos
icacls D:\PROJECTS\BuscaDatosPasajero
```

### Solución de Problemas Comunes

1. **Error 500 - Internal Server Error**:
   - Verificar logs en: `D:\PROJECTS\BuscaDatosPasajero\logs\wfastcgi.log`
   - Revisar Event Viewer → Windows Logs → Application
   - Ejecutar: `iisreset`

2. **Python no encontrado**:
   - Verificar variable PATH del sistema
   - Reinstalar con: `install_python_server_2022.bat`

3. **Problemas de permisos**:
   - Verificar que IIS_IUSRS tenga permisos en el directorio
   - Ejecutar: `icacls D:\PROJECTS\BuscaDatosPasajero /grant IIS_IUSRS:F /T`

4. **FastCGI no responde**:
   - Verificar configuración: `appcmd list config /section:system.webServer/fastCGI`
   - Reconfigurar con: `configure_fastcgi_server_2022.bat`

5. **Conflictos entre configuración manual y automática**:
   - **SOLUCIÓN**: Ejecutar `reset_and_cleanup_server_2022.bat`
   - Luego ejecutar `deploy_complete_server_2022.bat`
   - **PREVENCIÓN**: Siempre usar scripts automáticos desde el inicio

6. **Configuraciones duplicadas o conflictivas**:
   - Síntomas: Múltiples sitios, Application Pools duplicados
   - **SOLUCIÓN**: Ejecutar script de limpieza y empezar de nuevo
   - Verificar con: `appcmd list site` y `appcmd list apppool`

### 🔄 Flujo Recomendado para Evitar Conflictos

```
┌─────────────────────────────────────────┐
│ ¿Primera instalación?                   │
├─────────────────────────────────────────┤
│ SÍ  → deploy_complete_server_2022.bat   │
│ NO  → reset_and_cleanup_server_2022.bat │
│       ↓                                 │
│       deploy_complete_server_2022.bat   │
└─────────────────────────────────────────┘
```
