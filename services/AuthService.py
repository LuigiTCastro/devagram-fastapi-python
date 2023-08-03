from models.UserModel import UserLoginModel
from repositories.UserRepository import UserRepository
from services.UserService import UserService
from utils.AuthUtil import AuthUtil
from utils.JwtToken import JwtToken

userRepository = UserRepository()
authUtil = AuthUtil()
jwtToken = JwtToken()
userService = UserService()


class AuthService:

    async def login_service(self, user: UserLoginModel):
        try:
            wanted_user = await userRepository.find_user_by_email(user.email)

            if not wanted_user:
                return {
                    'message': 'User not found.',
                    'data': '',
                    'status': 401
                }

            if authUtil.decrypt_password(user.password, wanted_user['password']):
                wanted_user['id'] = str(wanted_user.pop('_id'))
                return {
                    'message': 'Login successfully realized.',
                    'data': wanted_user,
                    'status': 200
                }

            else:
                return {
                    'message': 'User not found.',
                    'data': '',
                    'status': 401
                }

        except Exception as error:
            print(error)

    async def get_logged_user(self, authorization: str):
        token = authorization.split(' ')[1]
        payload = jwtToken.decode_jwt_token(token)
        logged_user = await userService.find_user_by_id(payload['id'])
        result = logged_user['data']

        return result
