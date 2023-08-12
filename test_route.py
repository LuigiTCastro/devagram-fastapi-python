import motor.motor_asyncio
from datetime import datetime
from typing import List, Optional
from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel, Field, EmailStr
from decouple import config

from utils.AuthUtil import AuthUtil

router = APIRouter()
authUtil = AuthUtil()


def test_helper(test):
    return {
        'id': str(test['_id']),  # TOO NECESSARY
        'name': test['name'],
        'email': test['email'],
        'password': test['password'],
        # 'followers': [str(p) for p in test['followers']] if 'followers' in test else '',
        # 'following': [str(p) for p in test['following']] if 'following' in test else '',
        'followers': [str(p) for p in test.get('followers', [])],
        'following': [str(p) for p in test.get('following', [])],
        'total_followers': test.get('total_followers', None),
        'total_following': test.get('total_following', None),
        'datetime': test['datetime'] if 'datetime' in test else ''
    }


class TestModel(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    followers: List
    following: List
    total_followers: int
    total_following: int
    datetime: str

    class Config:
        json_schema_extra = {
            'test': {
                'name': 'string',
                'email': 'string',
                'password': 'string',
                'followers': 'List',
                'following': 'List',
                'total_followers': 'int',
                'total_following': 'int',
                'datetime': 'date'
            }
        }


class TestCreateModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    followers: List = []
    following: List = []
    total_followers: int = 0
    total_following: int = 0
    datetime: str = str(None)

    class Config:
        json_schema_extra = {
            'test': {
                'name': 'string',
                'email': 'string',
                'password': 'string',
                'followers': 'List',
                'following': 'List',
                'total_followers': 'int',
                'total_following': 'int',
                'datetime': 'date'
            }
        }

# If i to create a test of TestModel type, all the fields will be required.
# Therefore, we have a TestModel like base, but we use the TestCreateModel type, where it only has the attributes: name, email, password.
# However, using the TestCreateModel, but returning the TestHelper with all fields, will give an error, because the other fields are not exist.
    # How to fix this? We see two possibilities below:
        # 1) Using some service that increasing new attributes through of the Update;
        # 2) In the Create moment, pass a dict with the new attributes.

# __________________________________________________________________________________________

MONGODB_URL = config('MONGODB_URL')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
database = client.devagrampythoncluster
test_collection = database.get_collection('test')


async def find_test_repository(email: str):
    wanted_test = await test_collection.find_one({'email': email})
    return wanted_test


async def test_repository(test: TestCreateModel) -> dict:
    test.password = authUtil.encrypt_password(test.password)
    test.datetime = datetime.now()

    created_test = await test_collection.insert_one(test.__dict__)
    # test['password'] = authUtil.encrypt_password(test['password']) # Alternative
    # created_test = await test_collection.insert_one(test) # Alternative

    new_test = await test_collection.find_one({'_id': created_test.inserted_id})
    return test_helper(new_test)


async def test_service(test: TestCreateModel):
    try:
        wanted_test = await find_test_repository(test.email)

        if wanted_test is not None:
            return {
                'message': 'Test already exists.',
                'data': '',
                'status': 400
            }
        else:
            new_test = await test_repository(test)
            return {
                'message': 'Test successfully executed.',
                'data': new_test,
                'status': 201
            }

    except Exception as error:
        return {
            'message': 'Internal server error.',
            'data': str(error),
            'status': 500
        }


@router.post('/', tags=['Test'])
async def test_route(test: TestCreateModel = Depends(TestCreateModel)):
    try:
        # test_dict = test.dict() # Alternative
        # result = await test_service(test_dict) # Alternative
        result = await test_service(test)

        if not result['status'] == 201:
            raise HTTPException(status_code=result['status'], detail=result['message'])

        return result

    except Exception as error:
        print(error)
        raise error
