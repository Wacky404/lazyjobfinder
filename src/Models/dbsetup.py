from dotenv import load_dotenv
from pprint import pprint
from src.utils.logger import logger
import psycopg2
import os


load_dotenv()
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
)

cur = conn.cursor()


def db_setup(model: str = "initial.sql", cur=cur):
    with open(model, "r") as fd:
        cur.execute(fd.read())


if __name__ == '__main__':
    with open("initial.sql", "r") as fd:
        cur.execute(fd.read())
