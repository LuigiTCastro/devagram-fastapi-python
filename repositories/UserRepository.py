import motor.motor_asyncio
from decouple import config
from bson import ObjectId
from models.UserModel import UserCreateModel
from utils.AuthUtil import AuthUtil


# from utils.userHelper import userHelper

def user_helper(user):
    return {
        'id': user['_id'],
        'name': user['name'],
        'email': user['email'],
        'password': user['password'],
    }


MONGODB_URL = config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
database = client.devagrampythoncluster
user_collection = database.get_collection("user")

authUtil = AuthUtil()


class UserRepository:

    async def create_user(self, user: UserCreateModel) -> dict:
        user.password = authUtil.encrypt_password(user.password)
        user_created = await user_collection.insert_one(user.__dict__)
        new_user = await user_collection.find_one({'_id': user_created.inserted_id})

        return user_helper(new_user)
        # return {
        #     'id': str(user['_id']),
        #     'name': user['name'],
        #     'email': user['email'],
        #     'password': user['password'],
        # }

    async def list_users(self):
        return user_collection.find()

    async def find_user_by_email(email: str):
        user = user_collection.find_one({'email': email})

        if not user:
            print('User not found')

        return user_helper(user)

    async def find_user_by_id(id: str):
        user = await user_collection.find_one({'_id': ObjectId(id)})

        if not user:
            print('User not found')

        return user_helper(user)

    async def update_user(id: str, user_data: dict):
        user = await user_collection.find_one({"_id": ObjectId(id)})

        if user:
            updated_user = await user_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": user_data}
            )

        return user_helper(updated_user)

    async def delete_user(id: str):
        user = await user_collection.find_one({"_id": ObjectId(id)})

        if not user:
            print('user not found')

        await user_collection.delete_one({"_id": ObjectId(id)})
