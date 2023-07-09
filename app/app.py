import os
import asyncio
import fastapi
import jwt.exceptions
import pydantic_core
import jwt
from main import logger
from app import models
from app import auth
from app import db_logic

app = fastapi.FastAPI()

@app.get('/', tags=['ABOUT'])
async def hello():
    return {"Message": "This is the API for blogging app. Use /docs to access Swagger"}

@app.post("/signup", description="Make a POST-request with user data to sign up", tags=['SIGNUP'])
async def register(user: models.User):
    try:
        user.password = await auth.hash_password(user.password)
        if await db_logic.fetch_user(user.email):
            return {"Message": "The user already exists"}
        await db_logic.add_user(user)
        return {"Message": "User have been created"}
    except pydantic_core.ValidationError:
        return fastapi.HTTPException(status_code=400, detail="Incorrect request body. Please submit the correct data")
    except:
        logger.exception("An exception has occured")
        return fastapi.HTTPException(status_code=500, detail="An unexpected error with registration happened")

@app.get("/login", tags=["Login"], description="This endpoints takes email and password and returns JWT")
async def login(email: str = fastapi.Header(), password: str = fastapi.Header()):
    try:
        password = await auth.hash_password(password)
        user = await db_logic.fetch_user(email)
        if not user:
            return fastapi.HTTPException(status_code=400, detail="Invalid email or password. No record in the database")
        elif user.password != password:
            return fastapi.HTTPException(status_code=400, detail="Invalid password")

        token = await auth.generate_jwt(user)
        return token
    except:
        logger.exception("An exception has occured")
        return fastapi.HTTPException(status_code=500, detail="An unexpected error with login has occured. See logs for additional information")

@app.post("/blogs", tags=["BLOGPOSTS"], description="This endpoint provides RESTful interaction with blogs. Submit users JWT"
                                                    "with your requests to perform CRUDs")
async def create_post(post: models.BlogPost, token: str = fastapi.Header()):
    try:
        payload = await auth.validate_token(token)
        user = await db_logic.fetch_user(payload.email)
        post.author_id = user.id
        await db_logic.add_post(post)
        return {"Message": "Blogpost created successfully"}
    except pydantic_core.ValidationError:
        return fastapi.HTTPException(status_code=400, detail="Bad request")
    except jwt.exceptions.InvalidTokenError:
        return fastapi.HTTPException(status_code=402, detail="Invalid token. Use /login to get a new token")
    except:
        logger.exception("An exception has occured")
        return fastapi.HTTPException(status_code=500, detail="An unexpected error has occured on the server")

