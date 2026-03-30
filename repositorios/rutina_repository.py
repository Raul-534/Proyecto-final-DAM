class RutinaRepository:
    def __init__(self):
        self.db = DatabaseManager()

    def obtener_rutinas_usuario(self, id_usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT r.nombre as rutina_nombre, e.nombre as ejercicio, 
                       re.series, re.repeticiones, re.descanso
                FROM rutinas r
                JOIN rutina_ejercicios re ON r.id_rutina = re.id_rutina
                JOIN ejercicios e ON re.id_ejercicio = e.id_ejercicio
                WHERE r.id_usuario = %s
            """
            cursor.execute(query, (id_usuario,))
            return cursor.fetchall()
        finally:
            conn.close()