import os

from models.UserModel import UserCreateModel, UserUpdateModel
from providers.AWSProvider import AWSProvider
from repositories.UserRepository import UserRepository

userRepository = UserRepository()
awsProvider = AWSProvider()


class UserService:

    async def register_user(self, user: UserCreateModel, photo_path):
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

                try:
                    photo_url = awsProvider.s3_file_upload(
                        photo_path,
                        f'profile-photos/{new_user["id"]}.png'
                    )

                    new_user = await userRepository.update_user(new_user['id'], {'photo': photo_url})

                except Exception as error:
                    print(error)

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

    async def list_users(self):
        try:
            users = await userRepository.find_users()

            if not users:
                return {
                    'message': 'Users not found.',
                    'data': '',
                    'status': 404
                }

            return {
                'message': 'User found.',
                'data': users,
                'status': 200
            }

        except Exception as error:
            print(error)
            return {
                'message': 'Internal server error.',
                'data': str(error),
                'status': 500
            }

    async def update_logged_user(self, id: str, user_to_update: UserUpdateModel):
        try:
            wanted_user = await userRepository.find_user_by_id(id)

            if wanted_user is None:
                return {
                    'message': 'User not found.',
                    'data': '',
                    'status': 404
                }

            else:
                photo_upload = user_to_update.photo
                user_dict = user_to_update.__dict__
                # del user_dict['photo']

                try:
                    photo_path = f'file/{photo_upload.filename}.png'

                    with open(photo_path, 'wb+') as f:
                        f.write(photo_upload.file.read())

                    photo_url = awsProvider.s3_file_upload(
                        photo_path,
                        f'profile-photos/{id}.png'
                    )

                    os.remove(photo_path)

                except Exception as error:
                    print(error)

                user_dict['photo'] = photo_url if photo_url is not None else user_dict['photo']
                updated_user = await userRepository.update_user(id, user_dict)

                return {
                    'message': 'User updated',
                    'data': updated_user,
                    'status': 200
                }

        except Exception as error:
            return {
                'message': 'Internal server error.',
                'data': str(error),
                'status': 500
            }
