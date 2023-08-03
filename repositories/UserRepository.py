import motor.motor_asyncio
from decouple import config
# from bson import ObjectId
from bson.objectid import ObjectId
from models.UserModel import UserCreateModel
from utils.AuthUtil import AuthUtil
from helpers.UserHelper import user_helper


MONGODB_URL = config('MONGODB_URL')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
database = client.devagrampythoncluster
user_collection = database.get_collection('user')

authUtil = AuthUtil()


class UserRepository:

    async def create_user(self, user: UserCreateModel) -> dict:
        user.password = authUtil.encrypt_password(user.password)
        created_user = await user_collection.insert_one(user.__dict__)
        # .__dict__: converts the attributes of a class into a dictionary.

        new_user = await user_collection.find_one({'_id': created_user.inserted_id})
        return user_helper(new_user)

    async def find_users(self) -> dict:
        users_found = await user_collection.find()
        return user_helper(users_found)


    async def find_user_by_email(self, email: str):
        user = await user_collection.find_one({'email': email})
        return user

    async def find_user_by_id(self, id: str):
        user = await user_collection.find_one({'_id': ObjectId(id)})
        return user_helper(user)
        # ObjectId: is an object field created automatically by MongoDB to identify documents.

    async def update_user(self, id: str, user_data: dict):
        if 'password' in user_data:
            user_data['password'] = authUtil.encrypt_password(user_data['password'])

        user = await user_collection.find_one({"_id": ObjectId(id)})

        if user:
            await user_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": user_data}
            )

            updated_user = await user_collection.find_one({
                {"_id": ObjectId(id)}
            })

            return user_helper(updated_user)  # Check

        else:
            return None

    async def remove_user(self, id: str):
        user = await user_collection.find_one({"_id": ObjectId(id)})  # Check
        if user:
            await user_collection.delete_one({"_id": ObjectId(id)})
