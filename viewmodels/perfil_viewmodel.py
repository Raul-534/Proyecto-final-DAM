from repositorios.database import DatabaseManager # Asegúrate de que el nombre del archivo coincida

class PerfilViewModel:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def obtener_datos_perfil(self, nombre_usuario):
        """Busca los datos físicos del usuario por su nombre de usuario."""
        conn = self.db_manager.get_connection()
        if not conn: return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            # Primero obtenemos el ID del usuario
            query_id = "SELECT id FROM usuarios WHERE nombre = %s"
            cursor.execute(query_id, (nombre_usuario,))
            user = cursor.fetchone()
            
            if user:
                # Buscamos en la tabla perfiles usando 'id_usuario' (como en tu imagen)
                query_perfil = "SELECT * FROM perfiles WHERE id_usuario = %s"
                cursor.execute(query_perfil, (user['id'],))
                return cursor.fetchone()
            return None
        except Exception as e:
            print(f"❌ Error al obtener perfil: {e}")
            return None
        finally:
            conn.close()

    def guardar_o_actualizar_perfil(self, nombre_usuario, datos):
        """Inserta o actualiza los datos del perfil usando el patrón ON DUPLICATE KEY."""
        conn = self.db_manager.get_connection()
        if not conn: return False
        
        try:
            cursor = conn.cursor(dictionary=True)
            # 1. Obtener el ID real del usuario
            cursor.execute("SELECT id FROM usuarios WHERE nombre = %s", (nombre_usuario,))
            user_res = cursor.fetchone()
            if not user_res: return False
            
            user_id = user_res['id']

            # 2. SQL de inserción/actualización según las columnas de tu imagen
            # Columnas: id_usuario, peso, altura, edad, genero, objetivo, actividad
            sql = """
                INSERT INTO perfiles (id_usuario, peso, altura, edad, genero, objetivo, actividad)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                peso=%s, altura=%s, edad=%s, genero=%s, objetivo=%s, actividad=%s
            """
            
            valores = (
                user_id, datos['peso'], datos['altura'], datos['edad'], datos['genero'], datos['objetivo'], datos['actividad'],
                datos['peso'], datos['altura'], datos['edad'], datos['genero'], datos['objetivo'], datos['actividad']
            )
            
            cursor.execute(sql, valores)
            conn.commit()
            return True
            
        except Exception as e:
            print(f"❌ Error al guardar perfil: {e}")
            return False
        finally:
            conn.close()