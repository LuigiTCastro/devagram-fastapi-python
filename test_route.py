import motor
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
    }


class TestModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            'test': {
                'name': 'string',
                'email': 'string',
                'password': 'string'
            }
        }


MONGODB_URL = config('MONGODB_URL')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
database = client.devagrampythoncluster
test_collection = database.get_collection('test')


async def find_test_repository(email: str):
    wanted_test = await test_collection.find_one({'email': email})
    return wanted_test


async def test_repository(test: TestModel) -> dict:
    test.password = authUtil.encrypt_password(test.password)
    created_test = await test_collection.insert_one(test.__dict__)
    # test['password'] = authUtil.encrypt_password(test['password']) # Alternative
    # created_test = await test_collection.insert_one(test) # Alternative
    new_test = await test_collection.find_one({'_id': created_test.inserted_id})
    return test_helper(new_test)


async def test_service(test: TestModel):
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
async def test_route(test: TestModel = Depends(TestModel)):
    try:
        # test_dict = test.dict() # Alternative
        # result = await test_service(test_dict) # Alternative
        result = await test_service(test)

        if not result['status'] == 201:
            raise HTTPException(status_code=result['status'], detail=result['message'])

        return result

    except Exception as error:
        raise error
