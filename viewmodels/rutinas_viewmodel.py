from repositorios.database import DatabaseManager

class RutinasViewModel:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def obtener_ejercicios(self):
        conn = self.db_manager.get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT e.*, IFNULL(g.nombre_grupo, 'General') as nombre_grupo 
                FROM ejercicios e 
                LEFT JOIN grupos_musculares g ON e.id_grupo_muscular = g.id_grupo_muscular
            """
            cursor.execute(query)
            res = cursor.fetchall()
            print(f"DEBUG: Ejercicios encontrados: {len(res)}")
            return res
        except Exception as e:
            print(f"Error en SQL obtener_ejercicios: {e}")
            return []
        finally:
            conn.close()

    def obtener_rutina_por_id(self, id_rutina):
        """Obtiene los datos básicos (nombre, nivel) de una rutina específica para precargar campos."""
        conn = self.db_manager.get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT nombre, nivel FROM rutinas WHERE id_rutina = %s"
            cursor.execute(query, (id_rutina,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener cabecera de rutina: {e}")
            return None
        finally:
            conn.close()

    def guardar_rutina_completa(self, id_usuario, nombre, nivel, ejercicios):
        conn = self.db_manager.get_connection()
        if not conn: return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO rutinas (nombre, nivel, id_usuario) VALUES (%s, %s, %s)",
                (nombre, nivel, id_usuario)
            )
            id_rutina = cursor.lastrowid

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
            print(f"Error al guardar rutina: {e}")
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
        except Exception as e:
            print(f"Error al obtener detalles: {e}")
            return []
        finally:
            conn.close()

    def actualizar_rutina_completa(self, id_rutina, nombre, nivel, ejercicios):
        """Actualiza la cabecera y refresca la lista de ejercicios."""
        conn = self.db_manager.get_connection()
        if not conn: return False
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE rutinas SET nombre=%s, nivel=%s WHERE id_rutina=%s", (nombre, nivel, id_rutina))
            
            cursor.execute("DELETE FROM rutina_ejercicios WHERE id_rutina=%s", (id_rutina,))
            
            sql = "INSERT INTO rutina_ejercicios (id_rutina, id_ejercicio, series, repeticiones, descanso) VALUES (%s, %s, %s, %s, %s)"
            for ej in ejercicios:
                cursor.execute(sql, (id_rutina, ej['id'], ej['series'], ej['reps'], ej['descanso']))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error en actualizar_rutina_completa: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def listar_mis_rutinas(self, id_usuario):
        conn = self.db_manager.get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT id_rutina, nombre, nivel, id_usuario FROM rutinas WHERE id_usuario = %s"
            cursor.execute(query, (id_usuario,))
            resultados = cursor.fetchall()
            return resultados
        except Exception as e:
            print(f"Error en listar_mis_rutinas: {e}")
            return []
        finally:
            conn.close()
            
    def eliminar_rutina(self, id_rutina):
        conn = self.db_manager.get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM rutina_ejercicios WHERE id_rutina = %s", (id_rutina,))
            cursor.execute("DELETE FROM rutinas WHERE id_rutina = %s", (id_rutina,))
            conn.commit() 
            return True
        except Exception as e:
            print(f"ERROR AL ELIMINAR: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()