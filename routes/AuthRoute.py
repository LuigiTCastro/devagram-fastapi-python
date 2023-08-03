from models.UserModel import UserLoginModel
from services.AuthService import AuthService
from fastapi import APIRouter, Body, HTTPException
from utils.JwtToken import JwtToken

router = APIRouter()
authService = AuthService()
jwtToken = JwtToken()


# POST is used in a Login Route to be more secure by encapsulating sensitive data in the body.
@router.post('/login', response_description='Route to make Login')
async def login_route(user: UserLoginModel = Body(...)):
    result = await authService.login_service(user)

    if not result['status'] == 200:
        raise HTTPException(status_code=result['status'], detail=result['message'])

    data = result.get('data', {})  # Checks if 'data' is present in the results.
    user_id = data.get('id')  # Gets the user ID, if present.

    if not user_id:
        raise HTTPException(status_code=500, detail='ID of the user not found in the login results')

    # del data['password']  # Alternative
    # data['token'] = token  # Alternative
    del result['data']['password']
    token = jwtToken.generate_jwt_token(user_id)
    result['data']['token'] = token

    return result
