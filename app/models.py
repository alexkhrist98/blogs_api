import datetime
import pydantic

#this class contains all information about user. Extend by adding new field below
class User(pydantic.BaseModel):
    id: int = pydantic.Field(exclude=True, default=0, hide=True)
    first_name: str
    last_name: str
    email: pydantic.EmailStr
    password: str

class TokenPayload(pydantic.BaseModel):
    email: pydantic.EmailStr
    password: str
    exp: datetime.datetime = datetime.datetime.now() + datetime.timedelta(days=365)

class BlogPost(pydantic.BaseModel):
    id: int = pydantic.Field(default=0, exclude=True, hide=True)
    author_id: int = pydantic.Field(default=0, hide=True, exclude=True)
    title: str
    main_text: str
    tags: str = ""
    likes: int = pydantic.Field(default=0, exclude=True)
    dislikes: int = pydantic.Field(default=0, exclude=True)



