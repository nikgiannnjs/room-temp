import os #.env reader
import psycopg2 #postgresql library
from dotenv import load_dotenv #environment variables loader
from flask import Flask, request
from datetime import datetime
from queries import CREATE_ROOMS_TABLE, CREATE_TEMPS_TABLE, INSERT_ROOM_RETURN_ID, INSERT_TEMP, GLOBAL_AVG, GLOBAL_NUMBER_OF_DAYS


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
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_ROOMS_TABLE)
                cursor.execute(INSERT_ROOM_RETURN_ID , (name,))
                room_id = cursor.fetchone()[0] #brings back the first row the cursor has fetched. In this case, is the only one.
                return {"id": room_id , "message": f"Room {name} has been created"}, 201
    except Exception as e:
        print(f"Error at /api/room endpoint: {e}")
        return {"message": "Something went wrong while trying to add room."}, 500
        
@app.post("/api/temperature")
def add_temp():
    data = request.get_json()
    temperature = data["temperature"]
    room_id = data["room_id"]
    date = datetime.now()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_TEMPS_TABLE)
                cursor.execute(INSERT_TEMP , (room_id , temperature , date))
                cursor.execute("SELECT name FROM rooms WHERE id = %s;" , (room_id,))
                room = cursor.fetchone()[0]
                return {"message": f"{room} temperature has been added successfully."}, 201
    except Exception as e:
        print(f"Error at /api/temperature endpoint: {e}")
        return {"message": "Something went wrong while trying to add temperature."}, 500