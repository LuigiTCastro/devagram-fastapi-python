from typing import List, Optional
from pydantic import Field, BaseModel
from models.CommentsModel import CommentsModel
from models.UserModel import UserModel


class PostModel(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    user: UserModel = Field(...)
    photo: str = Field(...)
    subtitle: str = Field(...)
    date: str = Field(...)
    likes: int = Field(...)
    comments: List[CommentsModel] = Field(...)

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


class PostCreateModel(BaseModel):
    user: UserModel = Field(...)
    photo: str = Field(...)
    subtitle: str = Field(...)

    class Config:
        json_schema_extra = {
            'post': {
                'user': 'UserModel',
                'photo': 'string',
                'subtitle': 'string',
            }
        }
