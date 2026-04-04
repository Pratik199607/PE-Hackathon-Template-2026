from peewee import Model, PostgresqlDatabase
from peewee import DatabaseProxy
from app.config import Config 
db_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = db_proxy


def init_db(config):
    """
    Core DB initialization (Reusable everywhere)
    """
    db = PostgresqlDatabase(
        config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT,
    )

    db_proxy.initialize(db)
    return db


def init_db_with_flask(app):
    """
    Flask-specific wrapper
    """
    db = init_db(Config)

    @app.before_request
    def _connect():
        if db.is_closed():
            db.connect()

    @app.teardown_request
    def _close(exc):
        if not db.is_closed():
            db.close()

    return db