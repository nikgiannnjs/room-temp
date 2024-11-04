from flask import Flask
from dotenv import load_dotenv
from app.db import connection 

load_dotenv()  # Load environment variables from .env

def create_app():
    app = Flask(__name__)

    # Import routes and register blueprint
    from app.api.routes import temp_bp
    app.register_blueprint(temp_bp, url_prefix='/api')

    return app