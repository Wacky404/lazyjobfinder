""" ONLY RUN THIS SETUP SCRIPT ONCE """
from dotenv import load_dotenv
from pprint import pprint
from src.utils.logger import logger
from src.utils import paths
import psycopg2
import os

print(os.getenv("DATABASE_URL"))
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()


def db_setup(model: str = paths.initialsql, cur=cur) -> None:
    """
    Creates the base models of application.
    IMPORTANT!!!: Will drop existing tables, if they exist.

    Args:
        model: (str) path to sql file
    Returns:
        None
    """
    logger.debug(f"sql file being ran on db setup: {model}")
    with open(model, "r") as fd:
        cur.execute(fd.read())


if __name__ == '__main__':
    with open("./initial.sql", "r") as fd:
        cur.execute(fd.read())
