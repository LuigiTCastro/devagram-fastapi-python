from typing import Optional, List

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
    followers: List
    following: List
    total_followers: int
    total_following: int
    datetime: str

    class Config:
        json_schema_extra = {
            'user': {
                'name': 'string',
                'email': 'string',
                'password': 'string',
                'photo': 'string',
                'followers': 'List',
                'following': 'List',
                'total_followers': 'int',
                'total_following': 'int',
                'datetime': 'date'
            }
        }


@decoratorUtil.form_body
class UserCreateModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    # followers: List = []
    # following: List = []
    # total_followers: int = 0
    # total_following: int = 0
    # datetime: str = str(None)

    # FIX THIS!! [WHY ARE THESE ATTRIBUTES BEING REQUIRED, BUT NOT IN TEST_ROUTE?

    class Config:
        json_schema_extra = {
            'user': {
                'name': 'string',
                'email': 'string',
                'password': 'string',
                # 'followers': 'List',
                # 'following': 'List',
                # 'total_followers': 'int',
                # 'total_following': 'int',
                # 'datetime': 'date'
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
