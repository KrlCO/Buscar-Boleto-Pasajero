from flask import Flask, render_template, request, jsonify
import pyodbc
from datetime import datetime, timedelta
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Validar configuración al iniciar la aplicación
try:
    Config.validate_config()
    print("✓ Configuración validada correctamente")
except ValueError as e:
    print(f"❌ Error de configuración: {e}")
    print("💡 Asegúrate de:")
    print("   1. Crear un archivo .env basado en .env.example")
    print("   2. O configurar las variables de entorno en tu sistema")
    print("   3. Revisar el archivo config.example.py para más detalles")
    # En desarrollo, permitir continuar con valores por defecto
    if not Config.DEBUG:
        raise

class DatabaseConnection:
    def __init__(self):
        self.connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={app.config['DB_SERVER']};"
            f"DATABASE={app.config['DB_NAME']};"
            f"UID={app.config['DB_USER']};"
            f"PWD={app.config['DB_PASSWORD']};"
        )
    
    def get_connection(self):
        try:
            return pyodbc.connect(self.connection_string)
        except Exception as e:
            print(f"Error conectando a la base de datos: {e}")
            return None

class PassengerSearch:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def validate_client(self, co_clie):
        """Valida si el cliente existe en TMCLIE"""
        conn = self.db.get_connection()
        if not conn:
            return False, "Error de conexión a la base de datos"
        
        try:
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM TMCLIE WITH(NOLOCK) WHERE CO_CLIE = ?"
            cursor.execute(query, (co_clie,))
            count = cursor.fetchone()[0]
            return count > 0, "Cliente encontrado" if count > 0 else "Cliente no encontrado"
        except Exception as e:
            return False, f"Error en validación: {e}"
        finally:
            conn.close()
    
    def search_passenger_data(self, co_empr, co_clie, fe_docu_ini=None, fe_docu_fin=None, 
                                    co_rumb=None, co_dest_orig=None, co_dest_fina=None, 
                                    nu_secu=None, no_clie=None, nu_rucs=None, nu_dnis=None, 
                                    no_pasa=None, ti_serv=None, nu_asie=None, fe_viaj=None, 
                                    ho_viaj=None, ti_meto_pago=None):
        """Busca datos del pasajero usando el stored procedure sp_busca_pasajero"""
        conn = self.db.get_connection()
        if not conn:
            return None, "Error de conexión a la base de datos"
        
        try:
            cursor = conn.cursor()
            
            # Convertir fechas al formato datetime si están presentes
            fe_docu_ini_dt = None
            fe_docu_fin_dt = None
            fe_viaj_dt = None
            
            if fe_docu_ini:
                try:
                    if len(fe_docu_ini) == 8:  # YYYYMMDD
                        fe_docu_ini_dt = datetime.strptime(fe_docu_ini, '%Y%m%d')
                    elif len(fe_docu_ini) == 10:  # YYYY-MM-DD
                        fe_docu_ini_dt = datetime.strptime(fe_docu_ini, '%Y-%m-%d')
                except:
                    pass
            
            if fe_docu_fin:
                try:
                    if len(fe_docu_fin) == 8:  # YYYYMMDD
                        fe_docu_fin_dt = datetime.strptime(fe_docu_fin, '%Y%m%d')
                    elif len(fe_docu_fin) == 10:  # YYYY-MM-DD
                        fe_docu_fin_dt = datetime.strptime(fe_docu_fin, '%Y-%m-%d')
                except:
                    pass
            
            if fe_viaj:
                try:
                    if len(fe_viaj) == 8:  # YYYYMMDD
                        fe_viaj_dt = datetime.strptime(fe_viaj, '%Y%m%d')
                    elif len(fe_viaj) == 10:  # YYYY-MM-DD
                        fe_viaj_dt = datetime.strptime(fe_viaj, '%Y-%m-%d')
                except:
                    pass
            
            # Ejecutar el stored procedure
            cursor.execute("""
                EXEC sp_busca_pasajero 
                    @CO_EMPR = ?, 
                    @CO_CLIE = ?, 
                    @FE_DOCU_INI = ?, 
                    @FE_DOCU_FIN = ?, 
                    @CO_RUMB = ?, 
                    @CO_DEST_ORIG = ?, 
                    @CO_DEST_FINA = ?, 
                    @NU_SECU = ?, 
                    @NO_CLIE = ?, 
                    @NU_RUCS = ?, 
                    @NU_DNIS = ?, 
                    @NO_PASA = ?, 
                    @TI_SERV = ?, 
                    @NU_ASIE = ?, 
                    @FE_VIAJ = ?, 
                    @HO_VIAJ = ?, 
                    @TI_METO_PAGO = ?
            """, (
                co_empr, co_clie, fe_docu_ini_dt, fe_docu_fin_dt, 
                co_rumb, co_dest_orig, co_dest_fina, nu_secu, no_clie, 
                nu_rucs, nu_dnis, no_pasa, ti_serv, nu_asie, 
                fe_viaj_dt, ho_viaj, ti_meto_pago
            ))
            
            columns = [column[0] for column in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                row_dict = dict(zip(columns, row))
                # Formatear fechas para mejor visualización
                for key, value in row_dict.items():
                    if key.startswith('FE_') and value:
                        try:
                            if isinstance(value, datetime):
                                # Formato datetime a DD/MM/YYYY
                                row_dict[key] = value.strftime('%d/%m/%Y')
                            elif isinstance(value, str) and len(value) == 8:
                                # Formato YYYYMMDD a DD/MM/YYYY
                                formatted_date = f"{value[6:8]}/{value[4:6]}/{value[0:4]}"
                                row_dict[key] = formatted_date
                        except:
                            pass
                results.append(row_dict)
            
            return results, "Búsqueda completada"
        
        except Exception as e:
            return None, f"Error en búsqueda: {e}"
        finally:
            conn.close()

# Instancia global del buscador
searcher = PassengerSearch()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        
        # Campos obligatorios
        co_empr = (data.get('co_empr') or '').strip()
        co_clie = (data.get('co_clie') or '').strip()
        
        # Validar campos obligatorios
        if not co_empr:
            return jsonify({
                'success': False,
                'message': 'El código de empresa (CO_EMPR) es requerido'
            })
        
        if not co_clie:
            return jsonify({
                'success': False,
                'message': 'El código de cliente (CO_CLIE) es requerido'
            })
        
        # Campos opcionales del stored procedure
        fe_docu_ini = data.get('fe_docu_ini') or ''
        fe_docu_fin = data.get('fe_docu_fin') or ''
        co_rumb = (data.get('co_rumb') or '').strip() or None
        co_dest_orig = (data.get('co_dest_orig') or '').strip() or None
        co_dest_fina = (data.get('co_dest_fina') or '').strip() or None
        nu_secu = data.get('nu_secu') or None
        no_clie = (data.get('no_clie') or '').strip() or None
        nu_rucs = (data.get('nu_rucs') or '').strip() or None
        nu_dnis = (data.get('nu_dnis') or '').strip() or None
        no_pasa = (data.get('no_pasa') or '').strip() or None
        ti_serv = (data.get('ti_serv') or '').strip() or None
        nu_asie = data.get('nu_asie') or None
        fe_viaj = data.get('fe_viaj') or ''
        ho_viaj = (data.get('ho_viaj') or '').strip() or None
        ti_meto_pago = (data.get('ti_meto_pago') or '').strip() or None
        
        # Convertir números si están presentes
        try:
            if nu_secu and str(nu_secu).strip():
                nu_secu = int(nu_secu)
            else:
                nu_secu = None
        except:
            nu_secu = None
            
        try:
            if nu_asie and str(nu_asie).strip():
                nu_asie = int(nu_asie)
            else:
                nu_asie = None
        except:
            nu_asie = None
        
        # Validar cliente (opcional, no bloquea)
        client_exists, validation_msg = searcher.validate_client(co_clie)
        
        # Contar parámetros opcionales proporcionados para determinar el mensaje de espera
        optional_params_count = sum(1 for param in [
            fe_docu_ini, fe_docu_fin, co_rumb, co_dest_orig, co_dest_fina,
            nu_secu, no_clie, nu_rucs, nu_dnis, no_pasa, ti_serv, nu_asie,
            fe_viaj, ho_viaj, ti_meto_pago
        ] if param)
        
        # Buscar datos del pasajero usando el stored procedure
        results, search_msg = searcher.search_passenger_data(
            co_empr, co_clie, fe_docu_ini, fe_docu_fin, co_rumb, co_dest_orig,
            co_dest_fina, nu_secu, no_clie, nu_rucs, nu_dnis, no_pasa,
            ti_serv, nu_asie, fe_viaj, ho_viaj, ti_meto_pago
        )
        
        if results is None:
            return jsonify({
                'success': False,
                'message': search_msg
            })
        
        # Preparar información de parámetros de búsqueda
        search_params = {
            'co_empr': co_empr,
            'co_clie': co_clie,
            'fe_docu_ini': fe_docu_ini or 'Desde 2025-01-01',
            'fe_docu_fin': fe_docu_fin or 'Hasta hoy'
        }
        
        # Agregar parámetros opcionales que fueron proporcionados
        optional_params = {
            'co_rumb': co_rumb,
            'co_dest_orig': co_dest_orig,
            'co_dest_fina': co_dest_fina,
            'nu_secu': nu_secu,
            'no_clie': no_clie,
            'nu_rucs': nu_rucs,
            'nu_dnis': nu_dnis,
            'no_pasa': no_pasa,
            'ti_serv': ti_serv,
            'nu_asie': nu_asie,
            'fe_viaj': fe_viaj,
            'ho_viaj': ho_viaj,
            'ti_meto_pago': ti_meto_pago
        }
        
        for key, value in optional_params.items():
            if value:
                search_params[key] = value
        
        # Mensaje personalizado si no se encontraron resultados
        if len(results) == 0:
            no_results_message = (
                "No se encontraron registros con los datos proporcionados. "
                "Por favor, verifique que los datos sean correctos e intente nuevamente. "
                "Si los datos son correctos, no existe información en la base de datos para estos criterios."
            )
        else:
            no_results_message = None
        
        return jsonify({
            'success': True,
            'client_validation': {
                'exists': client_exists,
                'message': validation_msg
            },
            'results': results,
            'total_records': len(results),
            'search_params': search_params,
            'optional_params_count': optional_params_count,
            'no_results_message': no_results_message
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error interno: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)