import os

class Config:
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    DB_NAME = os.getenv("DATABASE_NAME")
    DB_HOST = os.getenv("DATABASE_HOST")
    DB_PORT = int(os.getenv("DATABASE_PORT", 5432))
    DB_USER = os.getenv("DATABASE_USER")
    DB_PASSWORD = os.getenv("DATABASE_PASSWORD")