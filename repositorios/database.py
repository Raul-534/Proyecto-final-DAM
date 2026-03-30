import mysql.connector

class DatabaseManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.config = {
                'host': 'localhost',
                'user': 'root',
                'password': '',
                'database': 'gimnasio_db',
                'port': 3306,
                'connect_timeout': 3
            }
        return cls._instance

    def get_connection(self):
        try:
            return mysql.connector.connect(**self.config)
        except Exception as e:
            print(f"❌ Error de conexión MySQL: {e}")
            return None