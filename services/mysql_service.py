import mysql.connector # type: ignore
import os
import time

class MySQLService:
    def __init__(self, host=None):
        self.host = host or os.getenv('MYSQL_HOST', 'localhost')
        self.user = os.getenv('MYSQL_USER', 'root')
        self.password = os.getenv('MYSQL_PASSWORD', 'Root@123')
        self.database = os.getenv('MYSQL_DATABASE', 'form_app')
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print(f"Connected to MySQL at {self.host}")
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            raise

    def _create_table_if_not_exists(self):
        """Create users table if it doesn't exist"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.connection.commit()
            print("Table 'users' created or already exists")
        except mysql.connector.Error as err:
            print(f"Error creating table: {err}")
            raise
    
    def save_user(self, name):
        if not self.connection:
            self.connect()
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO users (name) VALUES (%s)"
            cursor.execute(query, (name,))
            self.connection.commit()
            print(f"Saved user {name} to MySQL")
        except mysql.connector.Error as err:
            print(f"Error saving user to MySQL: {err}")
            raise
    
    def get_all_users(self):
        """Get all users from MySQL"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error fetching users: {err}")
            raise
    
    def close(self):
        if self.connection:
            self.connection.close()
            print("MySQL connection closed")
