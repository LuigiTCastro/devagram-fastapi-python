from typing import List, Optional
from pydantic import BaseModel, Field
# from models.PostModel import PostModel
from models.UserModel import UserModel


class CommentsModel(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    user: UserModel = Field(...)
    comment: str = Field(...)
    # post: PostModel = Field(...)
    date: str = Field(...)
    likes: int = Field(...)

    class Config:
        json_schema_extra = {
            'comment': {
                'id': 'string',
                'user': 'string',
                # 'post': 'string',
                'date': 'date',
                'likes': 'int'
            }
        }


