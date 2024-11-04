import psycopg2
from app.config import Config

# Database connection
try:
    connection = psycopg2.connect(
        host=Config.HOST,
        port=Config.PORT,
        database=Config.DATABASE,
        user=Config.USER,
        password=Config.PASSWORD
    )
    print("Database connection successful!")
except psycopg2.Error as e:
    print(f"Error connecting to the database: {e}")
    connection = None