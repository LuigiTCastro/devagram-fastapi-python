import motor
from bson import ObjectId

from helpers.PostHelper import post_helper
from models.PostModel import PostModel, PostCreateModel
from decouple import config

MONGODB_URL = config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
database = client.devagrampythoncluster
post_collection = database.get_collection('post')


class PostRepository:
    async def create_post(self, post: PostCreateModel) -> dict:
        created_post = await post_collection.insert_one(post.__dict__)
        new_post = await post_collection.find_one({'id': created_post.inserted_id})
        return post_helper(new_post)

    async def list_posts(self):
        return post_collection.find()

    async def find_post_by_email(self, email: str) -> dict:
        post = await post_collection.find_one({'email': email})
        return post_helper(post)

    async def find_post_by_id(self, id: str) -> dict:
        post = await post_collection.find_one({'_id': ObjectId(id)})
        return post_helper(post)

    async def update_post(self, id: str, post_data: dict):
        post = await post_collection.find_one({'_id': ObjectId(id)})

        if post:
            updated_post = await post_collection.update_one({'_id': ObjectId(id)}, {'$set': post_data})

        return post_helper(updated_post)

    async def remove_post(self, id: str):
        post = await post_collection.find_one({'_id': ObjectId(id)})
        if post:
            await post_collection.delete_one({'_id': ObjectId(id)})
