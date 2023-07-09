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

async def add_post(post: models.BlogPost):
    with await create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("BEGIN")
        cursor.execute("INSERT INTO posts(author_id, title, main_text, tags, likes, dislikes) VALUES (?, ?, ?, ?,?, ?)", (post.author_id,
                                                                                                                    post.title,
                                                                                                                    post.main_text,
                                                                                                                    post.tags,
                                                                                                                    post.likes,
                                                                                                                    post.dislikes, ))
        cursor.execute("COMMIT")
        conn.commit()

async def fetch_all_posts():
    try:
        with await create_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row
            cursor.execute("SELECT id, title, tags FROM posts")
            posts = cursor.fetchall()
            return posts
    except:
        logger.exception("An exception has occured")

async def fetch_one_post(id: int):
    with await create_connection() as conn:
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row
            cursor.execute("SELECT * FROM posts WHERE id = ?", (id,))
            post = cursor.fetchone()
            return post
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
        query2 = "CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                 "author_id INTEGER," \
                 "title TEXT," \
                 "main_text TEXT," \
                 "tags TEXT," \
                 "likes INTEGER," \
                 "dislikes INTEGER," \
                 "FOREIGN KEY (author_id) REFERENCES users(id))"
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("BEGIN")
        cursor.execute(query)
        cursor.execute(query2)
        cursor.execute("COMMIT")
        conn.commit()
        logger.info("Database is set up successfully")

if __name__ != "__main__":
    asyncio.create_task(set_up_db())

