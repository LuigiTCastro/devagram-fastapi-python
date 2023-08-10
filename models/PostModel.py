from typing import List, Optional

from fastapi import UploadFile
from pydantic import Field, BaseModel
from models.CommentsModel import CommentModel
from models.UserModel import UserModel
from utils.DecoratorUtil import DecoratorUtil

decoratorUtil = DecoratorUtil()


class PostModel(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    user_id: str = Field(...)
    photo: str = Field(...)
    subtitle: str = Field(...)
    date: str
    likes: List
    comments: List
    total_likes: int
    total_comments: int
    user: Optional[UserModel]

    class Config:
        json_schema_extra = {
            'post': {
                'id': 'string',
                'photo': 'string',
                'subtitle': 'string',
                'date': 'date',
                'likes': 'int',
                'comments': 'List[comments]',
            }
        }


@decoratorUtil.form_body
class PostCreateModel(BaseModel):
    photo: UploadFile = Field(...)
    subtitle: str = Field(...)

    class Config:
        json_schema_extra = {
            'post': {
                'photo': 'string',
                'subtitle': 'string',
            }
        }
