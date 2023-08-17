import os
from bson import ObjectId
from models.UserModel import UserCreateModel, UserUpdateModel
from providers.AWSProvider import AWSProvider
from repositories.UserRepository import UserRepository

userRepository = UserRepository()
awsProvider = AWSProvider()


class UserService:

    async def register_user(self, user: UserCreateModel, photo_path):
        # async def register_user(self, user: UserCreateModel):
        try:
            current_user = await userRepository.find_user_by_email(user.email)

            if current_user is not None:
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

    async def find_user_by_id(self, user_id: str):
        try:
            current_user = await userRepository.find_user_by_id(user_id)

            if not current_user:
                return {
                    'message': 'User not found.',
                    'data': '',
                    'status': 404
                }

            return {
                'message': 'User found.',
                'data': current_user,
                'status': 200
            }

        except Exception as error:
            print(error)
            return {
                'message': 'Internal server error.',
                'data': str(error),
                'status': 500
            }

    async def list_users(self, name: str = None):
        try:
            users_list = await userRepository.find_all_users(name)

            if not users_list:
                return {
                    'message': 'Users not found.',
                    'data': '',
                    'status': 404
                }

            return {
                'message': 'Users found.',
                'data': users_list,
                'status': 200
            }

        except Exception as error:
            print(error)
            return {
                'message': 'Internal server error.',
                'data': str(error),
                'status': 500
            }

    async def update_logged_user(self, user_id: str, user_data: UserUpdateModel):  # IT'S RETURNING 500. WHY?
        try:
            current_user = await userRepository.find_user_by_id(user_id)

            if current_user is None:
                return {
                    'message': 'User not found.',
                    'data': '',
                    'status': 404
                }

            else:  # Check if the provided email already exists in another user (excluding the current user)
                user_with_same_email = await userRepository.find_user_by_email(user_data.email)
                # WHERE IS THE ERROR?
                # find_user_by_email?
                # user_data.email?
                # user_with_same_email['_id'] != current_user['id']?
                if user_with_same_email and user_with_same_email['_id'] != current_user['id']:
                    return {
                        'message': 'This email is already in use by another user.',
                        'data': '',
                        'status': 401
                    }

                photo_upload = user_data.photo
                user_data_dict = user_data.__dict__
                # del user_data_dict['photo']

                try:
                    photo_path = f'file/{photo_upload.filename}.png'

                    with open(photo_path, 'wb+') as f:
                        f.write(photo_upload.file.read())

                    photo_url = awsProvider.s3_file_upload(
                        photo_path,
                        f'profile-photos/{user_id}.png'
                    )

                    os.remove(photo_path)

                except Exception as error:
                    print(f'{error} A')

                user_data_dict['photo'] = photo_url if photo_url is not None else user_data_dict['photo']
                updated_user = await userRepository.update_user(user_id, user_data_dict)

                return {
                    'message': 'User updated',
                    'data': updated_user,
                    'status': 200
                }

        except Exception as error:
            print(f'{error} B')
            return {
                'message': 'Internal server error.',
                'data': str(error),
                'status': 500
            }

    async def delete_user(self, user_id: str):
        user = await userRepository.find_user_by_id(user_id)

        if not user:
            return {
                'message': 'User not found.',
                'data': '',
                'status': 404
            }

    async def follow_or_unfollow(self, followed_user_id: str, follower_user_id: str):
        try:
            followed_user = await userRepository.find_user_by_id(followed_user_id)
            follower_user = await userRepository.find_user_by_id(follower_user_id)

            print(followed_user)
            print(follower_user)

            if not followed_user or not follower_user:
                return {
                    'message': 'User not found.',
                    'data': '',
                    'status': 404
                }

            if follower_user['following'].count(followed_user['id']) > 0:
                follower_user['following'].remove(followed_user['id'])
                followed_user['followers'].remove(follower_user['id'])
            else:
                follower_user['following'].append(ObjectId(followed_user['id']))
                followed_user['followers'].append(ObjectId(follower_user['id']))

            follower_user['total_following'] = len(follower_user['following'])
            followed_user['total_followers'] = len(followed_user['followers'])

            await userRepository.update_user(follower_user['id'], {
                'following': follower_user['following'],
                'total_following': follower_user['total_following']
            })

            await userRepository.update_user(followed_user['id'], {
                'followers': followed_user['followers'],
                'total_followers': followed_user['total_followers'],
            })

            return {
                'message': 'Followed user successfully.',
                'data': '',
                'status': 200
            }

        except Exception as error:
            return {
                'message': 'Internal server error.',
                'data': str(error),
                'status': 500
            }
