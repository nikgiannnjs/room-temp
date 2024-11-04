import os

class Config:
    HOST = os.getenv("HOST")
    PORT = os.getenv("POSTGRESQL_PORT")
    DATABASE = os.getenv("DATABASE")
    USER = os.getenv("POSTGRESQL_USER")
    PASSWORD = os.getenv("PASSWORD")