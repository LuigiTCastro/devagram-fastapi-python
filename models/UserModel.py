from pydantic import BaseModel, Field, EmailStr
from utils.DecoratorUtil import DecoratorUtil


decoratorUtil = DecoratorUtil()

class UserModel(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            'user': {
                'name': 'fulano',
                'email': 'fulano@email.com',
                'password': 'password123',
            }
        }


# @decoratorUtil.form_body
class UserCreateModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            'user': {
                'name': 'fulano',
                'email': 'fulano@email.com',
                'password': 'password123'
            }
        }


class UserLoginModel(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            'user': {
                'email': 'fulano@email.com',
                'password': 'password123',
            }
        }