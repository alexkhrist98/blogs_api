import pydantic

#this class contains all information about user. Extend by adding new field below
class User(pydantic.BaseModel):
    first_name: str
    last_name: str
    email: pydantic.EmailStr
    password: str
