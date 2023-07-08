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


async def fetch_user(user: models.User):
    with await create_connection() as conn:
        cursor = conn.cursor()
        conn.row_factory = sqlite3.Row
        cursor.execute("SELECT * FROM users WHERE emila=?", (user.email, ))
        user = cursor.fetchall()
        return user

async def add_user(user: models.User):
    with await create_connection() as conn:
        cursor = conn.cursor()
        conn.row_factory = sqlite3.Row
        cursor.execute("BEGIN")
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (user.first_name,
                                                                 user.last_name,
                                                                 user.email,
                                                                 user.password, ))
        conn.commit()
        logger.info("New user have been created")

async def set_up_db():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT,')")
