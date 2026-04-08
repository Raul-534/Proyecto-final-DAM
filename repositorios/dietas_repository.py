class DietasRepository:
    def __init__(self, db):
        self.db = db

    def obtener_macros(self, email):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM macros_usuario WHERE usuario_email = %s", (email,))
        res = cursor.fetchone()
        conn.close()
        return res if res else {"calorias_objetivo": 2000, "proteinas_objetivo": 150, "carbos_objetivo": 200, "grasas_objetivo": 60}

    def guardar_macros(self, email, cals, prot, carb, gras):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO macros_usuario (usuario_email, calorias_objetivo, proteinas_objetivo, carbos_objetivo, grasas_objetivo)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            calorias_objetivo=%s, proteinas_objetivo=%s, carbos_objetivo=%s, grasas_objetivo=%s
        """
        cursor.execute(query, (email, cals, prot, carb, gras, cals, prot, carb, gras))
        conn.commit()
        conn.close()
        
    def guardar_dieta_completa(self, email, nombre_dieta, objetivo, cals, prot, carb, gras):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO dietas (usuario_email, nombre, objetivo, kcal, proteína, carbos, grasas)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (email, nombre_dieta, objetivo, cals, prot, carb, gras))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al guardar dieta: {e}")
            return False
        finally:
            conn.close()