import secrets
import hashlib
import asyncio
from jwt import PyJWT
from main import logger

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