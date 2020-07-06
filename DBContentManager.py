import mysql.connector

class UseDatabase:
    def __init__(self, config: dict):
        """Expects Host/User/Password and Database to use"""
        self.configuration = config

    def __enter__(self) -> 'cursor':
        """Connect to the DB and create a cursor"""
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Destroy cursor and connection after commiting"""
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

class UseFXDatabase:
    pass
