from repositorios.database import DatabaseManager

class DietasViewModel:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def guardar_nueva_dieta(self, email, nombre_dieta, objetivo, kcal, p, c, g):
        """
        Guarda una nueva dieta buscando primero al usuario por su email.
        Retorna True si tiene éxito, False en caso contrario.
        """
        conn = self.db_manager.get_connection()
        if not conn: 
            return False
        
        try:
            cursor = conn.cursor(dictionary=True, buffered=True)
            
            cursor.execute("SELECT id_usuario FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if not user:
                return False

            sql = """
                INSERT INTO dietas (usuario_email, nombre, objetivo, kcal, proteína, carbos, grasas)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (email, nombre_dieta, objetivo, kcal, p, c, g)
            
            cursor.execute(sql, params)
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error en DietasViewModel (guardar): {e}")
            return False
        finally:
            conn.close()

    def eliminar_dieta(self, dieta_id):
        """Elimina una dieta usando el manager de base de datos"""
        conn = self.db_manager.get_connection()
        if not conn: 
            return False
        
        cursor = None
        try:
            cursor = conn.cursor(buffered=True)
            sql = "DELETE FROM dietas WHERE id = %s"
            
            cursor.execute(sql, (dieta_id,))
            conn.commit()
            
            return cursor.rowcount > 0
                
        except Exception as e:
            print(f"Error en DietasViewModel (eliminar): {e}")
            try:
                conn.rollback()
            except:
                pass
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def listar_dietas(self, email):
        conn = self.db_manager.get_connection()
        if not conn: 
            return []
        
        try:
            cursor = conn.cursor(dictionary=True, buffered=True)
            
            sql = "SELECT * FROM dietas WHERE usuario_email = %s ORDER BY fecha_creacion DESC"
            cursor.execute(sql, (email,))
            return cursor.fetchall()
            
        except Exception as e:
            print(f"Error en DietasViewModel (listar): {e}")
            return []
        finally:
            conn.close()