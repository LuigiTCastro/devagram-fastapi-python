from datetime import datetime
from typing import List
import motor.motor_asyncio
from bson import ObjectId
from helpers.PostHelper import post_helper
from models.PostModel import PostModel, PostCreateModel
from decouple import config

MONGODB_URL = config('MONGODB_URL')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
database = client.devagrampythoncluster
post_collection = database.get_collection('post')


class PostRepository:
    async def create_post(self, post: PostCreateModel, user_id) -> PostModel:
        post_dict = {
            'user_id': ObjectId(user_id),
            'subtitle': post.subtitle,
            'likes': [],
            'comments': [],
            'data': datetime.now()
        }

        created_post = await post_collection.insert_one(post_dict)
        new_post = await post_collection.find_one({'_id': created_post.inserted_id})
        return post_helper(new_post)

    async def find_posts(self) -> List[PostModel]:
        posts_found = await post_collection.aggregate([{
            "$lookup": {
                "from": "user",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user"
            }
        }])

        posts = []
        async for post in posts_found:
            posts.append(post_helper(post))

        return posts

    async def find_post_by_id(self, id: str) -> PostModel:
        post = await post_collection.find_one({'_id': ObjectId(id)})
        return post_helper(post)

    async def update_post(self, id: str, post_data: dict) -> PostModel:
        post = await post_collection.find_one({'_id': ObjectId(id)})

        if post:
            await post_collection.update_one({'_id': ObjectId(id)}, {'$set': post_data})
            updated_post = await post_collection.find_one({'_id': ObjectId(id)})
            return post_helper(updated_post)

    async def remove_post(self, id: str):
        post = await post_collection.find_one({'_id': ObjectId(id)})
        if post:
            await post_collection.delete_one({'_id': ObjectId(id)})
