import os #.env reader
import psycopg2 #postgresql library
from dotenv import load_dotenv #environment variables loader
from flask import Flask, request

#SQL Queries

CREATE_ROOMS_TABLE = "CREATE TABLE IF NOT EXISTS rooms (id SERIAL PRIMARY KEY , name VARCHAR(250));"
CREATE_TEMPS_TABLE = "CREATE TABLE IF NOT EXISTS temperatures (room_id INTEGER , temperature REAL, date TIMESTAMP , FOREIGN KEY(room_id) REFERENCES rooms(id) ON DELETE CASCADE);"
INSERT_ROOM_RETURN_ID = "INSERT INTO rooms (name) VALUES (%s) RETURNING id;"
INSERT_TEMP = "INSERT INTO temperatures (room_id , temperature , date) VALUES (%s , %s , %s);"
GLOBAL_NUMBER_OF_DAYS = "SELECT COUNT (DISTINCT DATE(date) AS days FROM temperatures);"
GLOBAL_AVG = "SELECT AVG(temperature) as average FROM temperatures;"


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

@app.post("/api/room")
def create_room():
    data = request.get_json()
    name = data["name"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ROOMS_TABLE)
            cursor.execute(INSERT_ROOM_RETURN_ID , (name,))
            room_id = cursor.fetchone()[0] #brings back the first row the cursor has fetched. In this case, is the only one.
            return {"id": room_id , "message": f"Room {name} has been created"}, 201
        
