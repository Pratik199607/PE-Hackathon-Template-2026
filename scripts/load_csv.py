from dotenv import load_dotenv
load_dotenv()
import csv
from peewee import chunked

from app.config import Config
from app.database import init_db
from app.models import Product


def load_csv(filepath):
    db = init_db(Config)

    db.connect()

    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with db.atomic():
        for batch in chunked(rows, 100):
            Product.insert_many(batch).execute()

    db.close()


if __name__ == "__main__":
    load_csv("products.csv")
    print("Data loaded 🚀")