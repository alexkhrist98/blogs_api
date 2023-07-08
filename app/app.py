import os
import asyncio
import fastapi
from main import logger

app = fastapi.FastAPI()

@app.get('/')
async def hello():
    return {"Message": "Hello"}