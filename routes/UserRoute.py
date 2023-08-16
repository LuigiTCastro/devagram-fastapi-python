import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile, File, Body
from middleware.JwtMiddleware import JwtMiddleware
from models.UserModel import UserCreateModel, UserUpdateModel
from services.AuthService import AuthService
from services.UserService import UserService
from utils.JwtToken import JwtToken

router = APIRouter()
userService = UserService()
jwtToken = JwtToken()
jwtMid = JwtMiddleware()
authService = AuthService()


@router.post('/register', response_description='Route to create a new user.')
async def post_user(photo: UploadFile, user: UserCreateModel = Depends(UserCreateModel)):
    # async def post_user(user: UserCreateModel = Depends(UserCreateModel)):
    try:
        print(photo.filename)
        photo_path = f'file/{photo.filename}.png'

        with open(photo_path, 'wb+') as f:
            f.write(photo.file.read())

        result = await userService.register_user(user, photo_path)
        # result = await userService.register_user(user)
        os.remove(photo_path)

        if not result['status'] == 201:
            raise HTTPException(status_code=result['status'], detail=result['message'])
            # raise (python) = throw (js)

        return result

    except Exception as error:
        print(error)
        raise error


@router.get(
    '/me',
    response_description='Route that returns information about the logged user.',
    dependencies=[Depends(JwtMiddleware.verify_token)]
)
async def get_logged_user_info(authorization: str = Header(default='')):
    try:
        print(authorization)
        token = authorization.split(' ')[1]
        payload = jwtToken.decode_jwt_token(token)
        result = await userService.find_user_by_id(payload['user_id'])

        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'], detail=result['message'])

        return result

    except Exception as error:
        raise error


@router.put(
    '/update',
    response_description='Route that updates the logged user.',
    dependencies=[Depends(JwtMiddleware.verify_token)]
)
async def put_user(
        authorization: str = Header(default=''),
        updated_user: UserUpdateModel = Depends(UserUpdateModel)
        # updated_user: UserUpdateModel = Body(...)
):
    try:
        logged_user = await authService.get_logged_user(authorization)
        result = await userService.update_logged_user(logged_user['id'], updated_user)

        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'], detail=result['message'])

        return result

    except Exception as error:
        raise error


@router.get(
    '/users',
    response_description='...',
    dependencies=[Depends(JwtMiddleware.verify_token)]
)
async def get_users():
    try:
        result = await userService.list_users()

        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'], detail=result['message'])

        return result

    except Exception as error:
        raise error


@router.put(
    '/follow/{followed_user_id}',
    response_description='Responsible route to follow or unfollow an user.',
    dependencies=[Depends(JwtMiddleware.verify_token)]
)
async def follow_or_unfollow(followed_user_id: str, authorization: str = Header(default='')):
    try:
        logged_user = await authService.get_logged_user(authorization)
        result = await userService.follow_or_unfollow(followed_user_id, logged_user['id'])

        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'], detail=result['message'])

        return result

    except Exception as error:
        print(error)
        raise error
