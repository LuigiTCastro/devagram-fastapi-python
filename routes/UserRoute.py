import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile, File
from middleware.JwtMiddleware import JwtMiddleware
from models.UserModel import UserCreateModel
from services.UserService import UserService
from utils.JwtToken import JwtToken

router = APIRouter()
userService = UserService()
jwtToken = JwtToken()


@router.post('/register', response_description='Route to create a new user.')
async def register_user(file: UploadFile, user: UserCreateModel = Depends(UserCreateModel)):
    try:
        print(file.filename)
        photo_path = f'file/{file.filename}.png'

        with open(photo_path, 'wb+') as f:
            f.write(file.file.read())

        result = await userService.register_user(user, photo_path)
        os.remove(photo_path)

        if not result['status'] == 201:
            raise HTTPException(status_code=result['status'], detail=result['message'])
            # raise (python) = throw (js)

        return result

    except Exception as error:
        # print(error)
        # raise HTTPException(status_code=500, detail='Server internal error.')
        raise error


@router.get(
    '/me',
    response_description='Route that returns information about the logged user.',
    dependencies=[Depends(JwtMiddleware.verify_token)]
)
async def get_logged_user_info(authorization: str = Header(default='')): # ITS NOT WORKING
    try:
        print(authorization)
        token = authorization.split(' ')[1]
        payload = JwtToken.decode_jwt_token(token)
        result = await userService.find_user_by_id(payload['user_id'])

        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'], detail=result['message'])

        return result

    except Exception as error:
        # raise HTTPException(status_code=500, detail='Server internal error.')
        raise error
