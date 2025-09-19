# 🚀 Despliegue en Servidor de Producción

## ⚡ Instalación Rápida (3 Pasos)

### 1️⃣ Copiar Archivos
Copiar toda la carpeta del proyecto al servidor en:
```
C:\Apps\BuscaDatosPasajero\
```

### 2️⃣ Ejecutar Instalación
```batch
# Instalar dependencias
install_dependencies.bat

# Configurar firewall (como Administrador)
configure_firewall.bat
```

### 3️⃣ Iniciar Servidor
```batch
# Iniciar aplicación
start_server.bat
```

## 📁 Archivos de Despliegue

| Archivo | Descripción |
|---------|-------------|
| `deploy_server.py` | Servidor de producción con Waitress |
| `install_dependencies.bat` | Instalación automática de dependencias |
| `configure_firewall.bat` | Configuración de firewall (puerto 5000) |
| `start_server.bat` | Script de inicio rápido |
| `DEPLOYMENT_GUIDE.md` | Guía detallada de despliegue |

## 🌐 Acceso a la Aplicación

### Desde el Servidor
```
http://localhost:5000
```

## 🔧 Configuración Requerida

### Base de Datos
Verificar configuración en `config.py`:
```python
DATABASE_CONFIG = {
    'server': 'SERIDOR',
    'database': 'Data Base',
    'username': 'user',
    'password': 'password'
}
```

### Firewall
Puerto 5000 debe estar abierto:
```powershell
# Verificar regla de firewall
netsh advfirewall firewall show rule name="Busca Boleto Pasajero Port 5000"
```

## 🧪 Pruebas de Conectividad

### Desde otra computadora
```powershell
# Probar conectividad IIS
Test-NetConnection -ComputerName IP -Port 9547

# Probar conectividad Flask
Test-NetConnection -ComputerName IP -Port 5000

# Acceder desde navegador (IIS recomendado)
http://IP:9547
```

## 📊 Características de Rendimiento

### Optimizaciones Implementadas
- ✅ Consultas SQL optimizadas con índices
- ✅ Servidor Waitress para producción
- ✅ Configuración multi-thread (6 threads)
- ✅ Límite de conexiones: 100 concurrentes


## 🔍 Funcionalidades de la Aplicación

### Búsqueda de Pasajeros
- **Campo obligatorio**: Código de Cliente
- **Filtros opcionales**: DNI, Tipo de Documento, Fechas
- **Resultados**: Campos principales + opción de ver todos

### Interfaz Web
- **Responsive**: Compatible con móviles y tablets
- **Traducción**: Nombres de campos en español
- **Formateo**: Fechas DD/MM/YYYY, importes con decimales
- **Validación**: Cliente debe existir en TMCLIE

## 🛠️ Mantenimiento

### Logs de la Aplicación
```
C:\Apps\BuscaDatosPasajero\app.log
```

### Reiniciar Servidor
```batch
# Detener: Ctrl+C en la ventana del servidor
# Iniciar: start_server.bat
```

### Actualizar Aplicación
1. Detener servidor
2. Hacer backup de `config.py`
3. Copiar nuevos archivos
4. Restaurar `config.py`
5. Reiniciar servidor

## 🆘 Solución de Problemas

### Error 0x80070585 (FastCGI IIS)
**Síntomas:** Error 500 en IIS con código 0x80070585, FastCgiModule, ExecuteRequestHandler

**Solución por Tipo de Error:**

#### 🔧 Error: "No se pudo encontrar <handler> scriptProcessor en la configuración de aplicación de <fastCGI>"
```bash
# Solución COMPLETA (RECOMENDADO - limpieza total y reconfiguración):
fix_scriptprocessor_complete.bat

# Solución alternativa (si la completa falla):
fix_scriptprocessor_mismatch.bat
```

#### 🔧 Otros errores 0x80070585:
```batch
# Solución completa y definitiva (RECOMENDADO)
fix_error_0x80070585_final.bat

# Diagnóstico y soluciones anteriores
diagnose_error_0x80070585.bat
fix_fastcgi_error.bat
verify_iis_deployment.bat
```

**Solución automática:**
```batch
# 1. Habilitar CGI en IIS (como administrador)
enable_iis_cgi.bat

# 2. Diagnosticar problema específico
diagnose_error_0x80070585.bat

# 3. Aplicar corrección completa
fix_fastcgi_error.bat

# 4. Verificar funcionamiento
verify_iis_deployment.bat
```

**Causas comunes:**
- IIS-CGI feature no habilitado
- FastCgiModule no cargado
- wfastcgi no instalado
- web.config mal configurado
- Permisos incorrectos
- Python no en PATH del sistema
- Handler FastCGI mal configurado
- **scriptProcessor mismatch** entre Handler y FastCGI Application

### Error 0x8007010b (FastCGI IIS)
**Síntomas:** Error 500 en IIS con código 0x8007010b, FastCgiModule, ExecuteRequestHandler

**Diagnóstico Avanzado:**
```bash
# Ejecutar en el servidor para análisis detallado
analyze_0x8007010b_remote.bat
```

**Solución Automática:**
```bash
# 1. Solución específica para rutas incorrectas (MÁS COMÚN)
fix_webconfig_paths.bat

# 2. Solución básica
fix_error_0x8007010b.bat

# 3. Solución avanzada (si persiste el error)
fix_0x8007010b_advanced.bat
```

**Causas específicas:**
- Archivos de aplicación faltantes o inaccesibles
- Permisos NTFS incorrectos en directorio de aplicación
- FastCGI Application mal configurada
- Application Pool con configuración incorrecta
- Rutas de Python o wfastcgi incorrectas en web.config
- Cache de IIS corrupto
- Dependencias Python faltantes o corruptas
- Errores en app_iis.py o app.py
- Error persistente después de configuración inicial

### Error 403.1 - Forbidden (0x80070005)

**Descripción:**
Error que indica que IIS no permite ejecutar scripts CGI/FastCGI en el directorio solicitado.

**Causas comunes:**
- Permisos de ejecución no configurados en IIS
- Handler Mappings incorrectos o faltantes
- Configuración de accessPolicy restrictiva
- Permisos de archivo insuficientes para IIS_IUSRS
- FastCGI Application mal configurada

**Solución Automática:**
```batch
# Script completo (ejecutar como administrador):
fix_error_403_forbidden.bat
```

**Pasos manuales (si el script falla):**
1. **Configurar permisos de ejecución:**
   - Abrir IIS Manager
   - Navegar a Default Web Site/BuscaDatosPasajero
   - Handler Mappings → Edit Feature Permissions
   - Habilitar: Read, Script, Execute

2. **Verificar Handler Mapping:**
   - Agregar nuevo Handler Mapping
   - Request path: *
   - Module: FastCgiModule
   - Executable: [Python Path]|[wfastcgi Path]

3. **Configurar FastCGI Application:**
   - FastCGI Settings en IIS
   - Agregar aplicación con Python path y wfastcgi
   - Configurar variables de entorno WSGI

### Error: "No se puede conectar"
- Verificar firewall: `configure_firewall.bat`
- Comprobar que el servidor esté ejecutándose
- Verificar IP y puerto

### Error: "Base de datos"
- Verificar credenciales en `config.py`
- Verificar driver ODBC instalado

### Error: "Dependencias"
- Re-ejecutar `install_dependencies.bat`
- Verificar Python 3.8+ instalado
- Comprobar entorno virtual

## 📞 Soporte

Para soporte técnico:
1. Revisar logs en `app.log`
2. Verificar conectividad de red
3. Comprobar estado del servicio
4. Contactar administrador del sistema

---