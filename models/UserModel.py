from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, Field, EmailStr
from utils.DecoratorUtil import DecoratorUtil

decoratorUtil = DecoratorUtil()


class UserModel(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    photo: str = Field(...)

    class Config:
        json_schema_extra = {
            'user': {
                'name': 'string',
                'email': 'string',
                'password': 'string',
                'photo': 'string'
            }
        }


@decoratorUtil.form_body
class UserCreateModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            'user': {
                'name': 'string',
                'email': 'string',
                'password': 'string'
            }
        }


class UserLoginModel(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            'user': {
                'email': 'string',
                'password': 'string',
            }
        }

@decoratorUtil.form_body
class UserUpdateModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    photo: UploadFile = Field(...)

    class Config:
        json_schema_extra = {
            'user': {
                'name': 'string',
                'email': 'string',
                'password': 'string',
                'photo': 'string'
            }
        }