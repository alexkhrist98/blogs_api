import pydantic

#this class contains all information about user. Extend by adding new field below
class User(pydantic.BaseModel):
    id: int = pydantic.Field(exclude=True)
    first_name: str
    last_name: str
    email: pydantic.EmailStr
    password: str
