import sqlite3
from backend.config import config

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = sqlite3.connect(config.DATABASE_URL.replace('sqlite:///', ''))
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
            print("Database connected successfully")
        except sqlite3.Error as err:
            print(f"Database connection failed: {err}")
            self.connection = None

    def execute_query(self, query, params=None, fetch=False):
        if not self.connection:
            raise Exception("No database connection")

        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or ())
            if fetch:
                result = cursor.fetchall()
                # Convert to dict-like objects for consistency
                return [dict(row) for row in result]
            else:
                self.connection.commit()
                result = cursor.rowcount
            return result
        except sqlite3.Error as err:
            self.connection.rollback()
            raise err
        finally:
            cursor.close()

    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed")

# Global database instance
db = Database()
