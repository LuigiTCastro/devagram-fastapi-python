from models.UserModel import UserLoginModel
from services.AuthService import AuthService
from fastapi import APIRouter, Body, HTTPException
from utils.JwtToken import JwtToken

router = APIRouter()
authService = AuthService()
jwtToken = JwtToken()


@router.post('/login', response_description='Route to make Login')
async def login_route(user: UserLoginModel = Body(...)):
    result = await authService.login_service(user)

    if not result['status'] == 200:
        raise HTTPException(status_code=result['status'], detail=result['message'])

    del result['data']['password']
    token = jwtToken.generate_jwt_token(['data']['id'])
    result['data']['token'] = token

    return result
