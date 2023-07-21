from models.UserModel import UserCreateModel
from repositories.UserRepository import UserRepository

userRepository = UserRepository()


class UserService:

    async def register_user(self, user: UserCreateModel):
        try:
            wanted_user = await userRepository.find_user_by_email(user.email)

            if wanted_user is not None:
                return {
                    'message': 'User already exists.',
                    'data': '',
                    'status': 400
                }

            else:
                new_user = await userRepository.create_user(user)
                return {
                    'message': 'User successfully registered.',
                    'data': new_user,
                    'status': 201
                }

        except Exception as error:
            return {
                'message': 'Internal server error.',
                'data': str(error),
                'status': 500
            }

    async def find_user_by_id(self, id: str):
        try:
            wanted_user = await userRepository.find_user_by_id(id)

            if not wanted_user:
                return {
                    'message': 'User not found.',
                    'data': '',
                    'status': 404
                }

            return {
                'message': 'User found.',
                'data': wanted_user,
                'status': 200
            }

        except Exception as error:
            print(error)
            return {
                'message': 'Internal server error.',
                'data': str(error),
                'status': 500
            }
