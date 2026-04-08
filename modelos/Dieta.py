class Dieta:
    def __init__(self, id, usuario_email, nombre, objetivo, kcal, proteina, carbos, grasas, fecha_creacion=None):
        self.id = id
        self.usuario_email = usuario_email
        self.nombre = nombre
        self.objetivo = objetivo
        self.kcal = kcal
        self.proteina = proteina
        self.carbos = carbos
        self.grasas = grasas
        self.fecha_creacion = fecha_creacion

    @staticmethod
    def from_db(row):
        """Convierte una fila de la DB en un objeto Dieta"""
        return Dieta(
            id=row['id'],
            usuario_email=row['usuario_email'],
            nombre=row['nombre'],
            objetivo=row['objetivo'],
            kcal=row['kcal'],
            proteina=row['proteína'],
            carbos=row['carbos'],
            grasas=row['grasas'],
            fecha_creacion=row.get('fecha_creacion')
        )