from flask import Flask
from dotenv import load_dotenv

from app.config import Config
from app.database import init_db_with_flask
from app.routes import register_routes


def create_app():
    # ✅ Load .env
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    # Init DB
    init_db_with_flask(app)

    # Routes
    register_routes(app)

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app