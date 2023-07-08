import os
import asyncio
import fastapi
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
    user.password = await auth.hash_password(user.password)
    if await db_logic.fetch_user(user):
        return {"Message": "The user already exists"}
    await db_logic.add_user(user)
    return {"Message": "User have been created"}

