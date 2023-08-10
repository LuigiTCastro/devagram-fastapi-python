from typing import List, Optional
from pydantic import BaseModel, Field
# from models.PostModel import PostModel
from models.UserModel import UserModel


class CommentModel(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    user: UserModel = Field(...)
    comment: str = Field(...)
    # post: PostModel = Field(...)
    date: str = Field(...)
    likes: int = Field(...)

    class Config:
        json_schema_extra = {
            'comments': {
                'id': 'string',
                'user': 'string',
                # 'post': 'string',
                'date': 'date',
                'likes': 'int'
            }
        }


class CommentCreateModel(BaseModel):
    comments: str = Field(...)

    class Config:
        json_schema_extra = {
            'post': {
                'comments': 'string'
            }
        }
