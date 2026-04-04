from dotenv import load_dotenv
load_dotenv()

from app.config import Config
from app.database import init_db
from app.models import Product


def init():
    db = init_db(Config)

    db.connect()
    db.create_tables([Product])
    db.close()


if __name__ == "__main__":
    init()
    print("Tables created ✅")