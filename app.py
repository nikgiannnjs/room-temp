import os #.env reader
import psycopg2 #postgresql library
from dotenv import load_dotenv #environment variables loader
from flask import Flask

load_dotenv()

app = Flask(__name__)

host = os.getenv("HOST")
port = os.getenv("POSTGRESQL_PORT")
database = os.getenv("DATABASE")
user = os.getenv("POSTGRESQL_USER")
password = os.getenv("PASSWORD")

try:
    connection = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    print("Database connection successful!")
except psycopg2.Error as e:
    print(f"Error connecting to the database: {e}")
    connection = None

@app.get("/")
def home():
    return "Hello!"