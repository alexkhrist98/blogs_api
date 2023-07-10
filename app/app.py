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
        raise fastapi.HTTPException(status_code=400, detail="Incorrect request body. Please submit the correct data")
    except:
        logger.exception("An exception has occured")
        raise fastapi.HTTPException(status_code=500, detail="An unexpected error with registration happened")

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
        raise fastapi.HTTPException(status_code=500, detail="An unexpected error with login has occured. See logs for additional information")

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
        raise fastapi.HTTPException(status_code=400, detail="Bad request")
    except jwt.exceptions.InvalidTokenError:
        raise fastapi.HTTPException(status_code=402, detail="Invalid token. Use /login to get a new token")
    except:
        logger.exception("An exception has occured")
        raise fastapi.HTTPException(status_code=500, detail="An unexpected error has occured on the server")

@app.get("/blogs", tags=['BLOGPOSTS'], description="this endpoint returns all blogposts")
async def read_all_posts():
    try:
        posts = await db_logic.fetch_all_posts()
        return posts
    except:
        logger.exception("An exception has occured")
        raise fastapi.HTTPException(status_code=500, detail="An unexpected error has occured")

@app.get("/blogs/{post_id}", tags=["BLOGPOSTS"], description="This endpoint returns a blogpost by its id, specify id in path")
async def read_post(post_id: int):
    try:
        if type(post_id) is not int:
            raise TypeError
        post = await db_logic.fetch_one_post(post_id)
        if not post:
            raise ValueError
        return post
    except TypeError:
        raise fastapi.HTTPException(status_code=400, detail="Invalid id. post_id should be integer")
    except ValueError:
        raise fastapi.HTTPException(status_code=404, detail="No post with such id")
    except:
        logger.exception("An exception has occured")
        raise fastapi.HTTPException(status_code=500, detail="An unexpected error has occured")

@app.patch("/blogs/{post_id}", tags=["BLOGPOSTS"], description="This endpoint uses patch to update count of likes and dislikes. "
                                                                   "Send like or dislike in the header")
async def update_reaction(post_id: int, token: str = fastapi.Header(), reaction: str = fastapi.Header()):
    try:
        payload = await auth.validate_token(token)
        post = await db_logic.fetch_one_post(post_id)
        if not post:
            raise ValueError
        post = models.BlogPost.parse_obj(post)
        user = await db_logic.fetch_user(user_id=post.author_id)
        if not user:
            pass
        elif user.email == payload.email:
            raise PermissionError

        if reaction.lower() == "like":
            post.likes += 1
        elif reaction.lower() == "dislike":
            post.dislikes += 1
        else:
            raise ValueError
        await db_logic.update_reaction(post)
        return {"Message": "Reaction was updated successfully"}
    except ValueError:
        logger.exception("An exception has occured")
        raise fastapi.HTTPException(status_code=400, detail="Invalid post id or reaction header")
    except jwt.exceptions.InvalidTokenError:
        raise fastapi.HTTPException(status_code=402, detail="Something in wrong with your token")
    except PermissionError:
        raise fastapi.HTTPException(status_code=403, detail="Permission denied. You can't like or dislike your own posts")
    except Exception:
        logger.exception("An exception has occured")
        raise fastapi.HTTPException(status_code=500, detail="An unexpected error has occured")
