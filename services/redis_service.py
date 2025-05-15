import redis
import os
import time

class RedisService:
    def __init__(self, host=None):
        self.host = host or os.getenv('REDIS_HOST', 'localhost')
        self.port = int(os.getenv('REDIS_PORT', 6379))
        self.db = int(os.getenv('REDIS_DB', 0))
        self.connection = None
        self.connect()

    def connect(self):
        """Connect to Redis with retry logic"""
        retries = 5
        for _ in range(retries):
            try:
                self.connection = redis.Redis(
                    host=self.host,
                    port=self.port,
                    db=self.db,
                    decode_responses=True
                )
                self.connection.ping()
                print(f"Connected to Redis at {self.host}:{self.port}")
                break
            except redis.ConnectionError as err:
                print(f"Error connecting to Redis: {err}. Retrying...")
                time.sleep(5)
        else:
            print("Failed to connect to Redis after several retries.")
            raise Exception("Unable to connect to Redis.")

    def save_user(self, name):
        if not self.connection:
            self.connect()
        try:
            self.connection.lpush('users', name)
           # print(f"Saved user {name} to Redis")
        except redis.RedisError as err:
            print(f"Error saving user to Redis: {err}")
            raise

    def get_all_users(self):
        if not self.connection:
            self.connect()
        try:
            return self.connection.lrange('users', 0, -1)
        except redis.RedisError as err:
            print(f"Error fetching users from Redis: {err}")
            raise

    def close(self):
        if self.connection:
            self.connection.close()
            print("Redis connection closed")
