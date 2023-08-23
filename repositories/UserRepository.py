import motor.motor_asyncio
from datetime import datetime
from typing import List
from decouple import config
from bson import ObjectId
from bson.objectid import ObjectId
from models.UserModel import UserCreateModel, UserModel
from utils.AuthUtil import AuthUtil
from helpers.UserHelper import user_helper

MONGODB_URL = config('MONGODB_URL')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
database = client.devagrampythoncluster
user_collection = database.get_collection('user')

authUtil = AuthUtil()


class UserRepository:

    async def create_user(self, user: UserCreateModel) -> UserModel:
        user.password = authUtil.encrypt_password(user.password)
        user_dict = {
            'name': user.name,
            'email': user.email,
            'password': user.password,
            'followers': [],
            'following': [],
            # 'posts': [],
            'total_followers': 0,
            'total_following': 0,
            # 'total_posts': 0,
            'datetime': datetime.now()
        }
        created_user = await user_collection.insert_one(user_dict)
        # .__dict__: converts the attributes of a class into a dictionary.

        new_user = await user_collection.find_one({'_id': created_user.inserted_id})
        return user_helper(new_user)

    async def find_all_users(self, name: str = None) -> List:
        users_found = await user_collection.find({
            'name': {
                '$regex': name,
                '$options': 'i'  # i: case insensitive
            }
        }).to_list(length=None)

        users_filtered = []

        for user in users_found:
            if name.lower() in user['name'].lower():
                users_filtered.append(user_helper(user))

        return users_filtered

    async def find_user_by_email(self, email: str):
        user = await user_collection.find_one({'email': email})
        return user

    async def find_user_by_id(self, user_id: str):
        user = await user_collection.find_one({'_id': ObjectId(user_id)})
        return user_helper(user)
        # ObjectId: is an object field created automatically by MongoDB to identify documents.

    async def update_user(self, user_id: str, user_data: dict):
        if 'password' in user_data:
            user_data['password'] = authUtil.encrypt_password(user_data['password'])

        user = await user_collection.find_one({"_id": ObjectId(user_id)})

        if user:
            await user_collection.update_one(
                {"_id": ObjectId(user_id)}, {"$set": user_data}
            )

            updated_user = await user_collection.find_one({
                {"_id": ObjectId(user_id)}
            })

            return user_helper(updated_user)  # Check

        else:
            return None

    async def remove_user(self, user_id: str):
        user = await user_collection.find_one({"_id": ObjectId(user_id)})  # Check
        if user:
            await user_collection.delete_one({"_id": ObjectId(user_id)})