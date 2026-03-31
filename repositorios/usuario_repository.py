import bcrypt
from repositorios.database import DatabaseManager

class UsuarioRepository:
    def __init__(self):
        self.db = DatabaseManager()

    def registrar_usuario(self, nombre, email, password):
        conn = self.db.get_connection()
        if not conn: return False
        cursor = conn.cursor()
        try:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            query = "INSERT INTO usuarios (nombre, email, contrasena) VALUES (%s, %s, %s)"
            cursor.execute(query, (nombre, email, hashed))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    def login(self, email, password):
        conn = self.db.get_connection()
        if not conn: return None
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user and bcrypt.checkpw(password.encode('utf-8'), user['contrasena'].encode('utf-8')):
                return user
            return None
        finally:
            conn.close()
            
    def actualizar_password(self, email, nueva_password):
        conn = self.db.get_connection()
        if not conn: return False
        cursor = conn.cursor()
        try:
            # Encriptamos la nueva contraseña igual que en el registro
            hashed = bcrypt.hashpw(nueva_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            query = "UPDATE usuarios SET contrasena = %s WHERE email = %s"
            cursor.execute(query, (hashed, email))
            conn.commit()
            return cursor.rowcount > 0 # Devuelve True si se encontró el email y se actualizó
        except Exception as e:
            print(f"Error al actualizar: {e}")
            return False
        finally:
            conn.close()