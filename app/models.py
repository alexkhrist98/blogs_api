import pydantic

#this class contains all information about user. Extend by adding new field below
class User(pydantic.BaseModel):
    id: int = pydantic.Field(exclude=True, default=0)
    first_name: str
    last_name: str
    email: pydantic.EmailStr
    password: str

class TokenPayload(pydantic.BaseModel):
    email: pydantic.EmailStr
    password: str
    exp: int = 9999999


