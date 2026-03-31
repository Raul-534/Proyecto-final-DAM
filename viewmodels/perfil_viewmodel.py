from repositorios.database import DatabaseManager

class PerfilViewModel:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def obtener_datos(self, nombre_usuario):
        conn = self.db_manager.get_connection()
        if not conn: return None
        try:
            #buffered=True es vital para evitar errores de lectura
            cursor = conn.cursor(dictionary=True, buffered=True)
            cursor.execute("SELECT id_usuario FROM usuarios WHERE nombre = %s", (nombre_usuario,))
            user = cursor.fetchone()
            if user:
                cursor.execute("SELECT * FROM perfiles WHERE id_usuario = %s", (user['id_usuario'],))
                return cursor.fetchone()
            return None
        finally:
            conn.close()

    def guardar_datos(self, nombre_usuario, d):
        conn = self.db_manager.get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor(dictionary=True, buffered=True)
            cursor.execute("SELECT id_usuario FROM usuarios WHERE nombre = %s", (nombre_usuario,))
            user = cursor.fetchone()
            if not user: return False

            sql = """
                INSERT INTO perfiles (id_usuario, peso, altura, edad, genero, objetivo, actividad)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                peso=%s, altura=%s, edad=%s, genero=%s, objetivo=%s, actividad=%s
            """
            params = (user['id_usuario'], d['peso'], d['altura'], d['edad'], d['genero'], d['objetivo'], d['actividad'],
                      d['peso'], d['altura'], d['edad'], d['genero'], d['objetivo'], d['actividad'])
            cursor.execute(sql, params)
            conn.commit()
            return True
        finally:
            conn.close()