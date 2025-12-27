import mysql.connector
from mysql.connector import pooling
from config import Config

class Database:
    _connection_pool = None

    @staticmethod
    def get_pool():
        if Database._connection_pool is None:
            try:
                Database._connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name="mypool",
                    pool_size=5,
                    host=Config.DB_HOST,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    database=Config.DB_NAME
                )
            except mysql.connector.Error as err:
                print(f"Error initializing connection pool: {err}")
                return None
        return Database._connection_pool

    @staticmethod
    def get_connection():
        pool = Database.get_pool()
        if pool:
            try:
                return pool.get_connection()
            except mysql.connector.Error as err:
                print(f"Error getting connection from pool: {err}")
                return None
        return None

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',        # Or '127.0.0.1'
            user='user',             # Make sure this matches docker-compose
            password='userpassword', # Make sure this matches docker-compose
            database='OnlineBookstore'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"❌ DATABASE CONNECTION ERROR: {err}") # <--- Look for this in terminal
        return None