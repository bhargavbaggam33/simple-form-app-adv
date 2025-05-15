import mysql.connector
import os
import time

class MySQLService:
    def __init__(self):
        self.host = os.getenv("MYSQL_HOST", "mysql")
        self.port = int(os.getenv("MYSQL_PORT", 3306))
        
        # Read secrets
        self.user = self._read_secret("/run/secrets/mysql_user")
        self.password = self._read_secret("/run/secrets/mysql_password")
        self.database = self._read_secret("/run/secrets/mysql_database")

        self.connection = None
        self.connect()

    def _read_secret(self, path):
        try:
            with open(path, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"Secret file not found: {path}")
            raise

    def connect(self):
        """Connect to MySQL with retry logic"""
        retries = 5
        for _ in range(retries):
            try:
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    auth_plugin='caching_sha2_password'
                )
                print(f"Connected to MySQL at {self.host}")
                self._create_table_if_not_exists()  # Ensure table is created if it doesn't exist
                break
            except mysql.connector.Error as err:
                print(f"Error connecting to MySQL: {err}. Retrying...")
                time.sleep(5)
        else:
            print("Failed to connect to MySQL after several retries.")
            raise Exception("Unable to connect to MySQL.")

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
           # print(f"Saved user {name} to MySQL")
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
