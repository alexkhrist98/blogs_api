import secrets
import hashlib
import asyncio
from jwt import PyJWT
from main import logger
from app import models

async def generate_secret_key():
    global SECRET_KEY
    SECRET_KEY = secrets.token_hex()
    logger.info("Secret key is generated")
    return SECRET_KEY

if __name__ != "__main__":
    asyncio.create_task(generate_secret_key())

async def hash_password(password: str):
    try:
        hasher = hashlib.sha256()
        hasher.update(password.encode())
        password_hash = hasher.hexdigest()
        return password_hash
    except TypeError:
        try:
            password = str(password).encode()
            hasher = hashlib.sha256()
            hasher.update(password)
            password_hash = hasher.hexdigest()
            return password_hash
        except:
            logger.exception("An exception has occured")
    except ValueError:
        logger.error("Invalid value for the password. Use string")

async def generate_jwt(user: models.User):
    try:
        payload = models.TokenPayload(email=user.email, password=user.password)
        payload = dict(payload)
        token = PyJWT().encode(payload=payload, key=SECRET_KEY)
        return token
    except:
        logger.exception("An exception has occured")




