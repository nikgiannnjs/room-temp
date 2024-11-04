from flask import Blueprint, request
from app.db import connection
from datetime import datetime
from app.db.queries import CREATE_ROOMS_TABLE, CREATE_TEMPS_TABLE, INSERT_ROOM_RETURN_ID, INSERT_TEMP

api_bp = Blueprint('api', __name__)

@api_bp.route('/room', methods=['POST'])
def create_room():
    data = request.get_json()
    name = data["name"]
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_ROOMS_TABLE)  # Create table if not exists
                cursor.execute(INSERT_ROOM_RETURN_ID, (name,))
                room_id = cursor.fetchone()[0]
                return {"id": room_id, "message": f"Room {name} has been created"}, 201
    except Exception as e:
        print(f"Error at /room endpoint: {e}")
        return {"message": "Failed to create room"}, 500


@api_bp.route('/temperature', methods=['POST'])
def add_temp():
    data = request.get_json()
    temperature = data["temperature"]
    room_id = data["room_id"]
    date = datetime.now()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_TEMPS_TABLE)  # Create table if not exists
                cursor.execute(INSERT_TEMP, (room_id, temperature, date))
                cursor.execute("SELECT name FROM rooms WHERE id = %s;", (room_id,))
                room_name = cursor.fetchone()[0]
                return {"message": f"Temperature for {room_name} added successfully."}, 201
    except Exception as e:
        print(f"Error at /temperature endpoint: {e}")
        return {"message": "Failed to add temperature"}, 500