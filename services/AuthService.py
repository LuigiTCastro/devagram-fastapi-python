from models.UserModel import UserLoginModel
from repositories.UserRepository import UserRepository
from utils.AuthUtil import AuthUtil

userRepository = UserRepository()
authUtil = AuthUtil()


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
