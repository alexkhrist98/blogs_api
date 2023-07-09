import sqlite3
import asyncio
from main import logger
from app import models
from app import models


DB_NAME = "blogs_api.db"

async def create_connection():
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except:
        logger.error("Cannot connect to the database")


async def fetch_user(email: str):
    try:
        with await create_connection() as conn:
            cursor = conn.cursor()
            conn.row_factory = sqlite3.Row
            cursor.row_factory = sqlite3.Row
            cursor.execute("SELECT * FROM users WHERE email=?", (email, ))
            user = cursor.fetchone()
            user = models.User.parse_obj(dict(user))

            return user
    except:
        logger.exception("An exception has occured")

async def add_user(user: models.User):
    try:
        with await create_connection() as conn:
            cursor = conn.cursor()
            conn.row_factory = sqlite3.Row
            cursor.execute("BEGIN")
            cursor.execute("INSERT INTO users (first_name, last_name, email, password)"
                           " VALUES (?, ?, ?, ?)", (user.first_name,
                                                                     user.last_name,
                                                                     user.email,
                                                                     user.password, ))
            conn.commit()
            logger.info("New user have been created")
    except:
        logger.exception("An exception has occured")

async def set_up_db():
    with await create_connection() as conn:
        cursor = conn.cursor()
        query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "first_name TEXT," \
                "last_name TEXT," \
                "email TEXT," \
                "password TEXT)"
        cursor.execute("BEGIN")
        cursor.execute(query)
        cursor.execute("COMMIT")
        conn.commit()
        logger.info("Database is set up successfully")

if __name__ != "__main__":
    asyncio.create_task(set_up_db())

