from repositorios.database import DatabaseManager

class RutinasViewModel:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def obtener_ejercicios(self):
        conn = self.db_manager.get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            # JOIN usando los nombres de tu tabla 'grupos_musculares'
            query = """
                SELECT e.*, g.nombre_grupo 
                FROM ejercicios e 
                JOIN grupos_musculares g ON e.id_grupo_muscular = g.id_grupo_muscular
            """
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            conn.close()

    def guardar_rutina_completa(self, id_usuario, nombre, nivel, ejercicios):
        conn = self.db_manager.get_connection()
        if not conn: return False
        cursor = conn.cursor()
        try:
            # Insertar en tabla 'rutinas'
            cursor.execute(
                "INSERT INTO rutinas (nombre, nivel, id_usuario) VALUES (%s, %s, %s)",
                (nombre, nivel, id_usuario)
            )
            id_rutina = cursor.lastrowid

            # Insertar en 'rutina_ejercicios'
            sql_detalles = """
                INSERT INTO rutina_ejercicios (id_rutina, id_ejercicio, series, repeticiones, descanso)
                VALUES (%s, %s, %s, %s, %s)
            """
            for ej in ejercicios:
                cursor.execute(sql_detalles, (
                    id_rutina, ej['id'], ej['series'], ej['reps'], ej['descanso']
                ))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
            
    def obtener_detalles_rutina(self, id_rutina):
        """Devuelve los ejercicios configurados para una rutina específica."""
        conn = self.db_manager.get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT re.*, e.nombre 
                FROM rutina_ejercicios re
                JOIN ejercicios e ON re.id_ejercicio = e.id_ejercicio
                WHERE re.id_rutina = %s
            """
            cursor.execute(query, (id_rutina,))
            return cursor.fetchall()
        finally:
            conn.close()

    def actualizar_rutina_completa(self, id_rutina, nombre, nivel, ejercicios):
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        try:
            # 1. Actualizar cabecera
            cursor.execute("UPDATE rutinas SET nombre=%s, nivel=%s WHERE id_rutina=%s", (nombre, nivel, id_rutina))
            # 2. Borrar ejercicios actuales para re-insertar la nueva selección
            cursor.execute("DELETE FROM rutina_ejercicios WHERE id_rutina=%s", (id_rutina,))
            # 3. Insertar nuevos
            sql = "INSERT INTO rutina_ejercicios (id_rutina, id_ejercicio, series, repeticiones, descanso) VALUES (%s, %s, %s, %s, %s)"
            for ej in ejercicios:
                cursor.execute(sql, (id_rutina, ej['id'], ej['series'], ej['reps'], ej['descanso']))
            conn.commit()
            return True
        except:
            conn.rollback()
            return False
        finally:
            conn.close()