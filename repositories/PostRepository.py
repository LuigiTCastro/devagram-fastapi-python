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
            'date': datetime.now()
        }

        created_post = await post_collection.insert_one(post_dict)
        new_post = await post_collection.find_one({'_id': created_post.inserted_id})
        return post_helper(new_post)

    async def find_all_posts(self) -> List[PostModel]:
        posts_found_cursor = post_collection.aggregate([{
            "$lookup": {
                "from": "user",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user"
            }
        }])

        # Convert the cursor to a list
        posts_found = await posts_found_cursor.to_list(length=None)

        posts_collection = []
        for post in posts_found:
            posts_collection.append(post_helper(post))

        return posts_collection

    async def find_all_user_posts(self, user_id: str) -> List[PostModel]:
        posts_found = await post_collection.find({'user_id': ObjectId(user_id)}).to_list(length=None)

        posts_collection = []

        for post in posts_found:
            posts_collection.append(post_helper(post))

        return posts_collection

    # async def find_all_user_posts(self, user_id: str) -> List[PostModel]:
    #     posts_found = post_collection.aggregate([
    #         {
    #             "$match": {
    #                 "user_id": ObjectId(user_id)
    #             }
    #         },
    #         {
    #             "$lookup": {
    #                 "from": "user",
    #                 "localField": "user_id",
    #                 "foreignField": "_id",
    #                 "as": "user"
    #             }
    #         }
    #     ])
    #
    #     posts_collection = []
    #
    #     async for post in posts_found:
    #         posts_collection.append(post_helper(post))
    #
    #     return posts_collection

    async def find_post_by_id(self, post_id: str) -> PostModel:
        post = await post_collection.find_one({'_id': ObjectId(post_id)})
        return post_helper(post)

    async def update_post(self, post_id: str, post_data: dict) -> PostModel:
        post = await post_collection.find_one({'_id': ObjectId(post_id)})

        if post:
            await post_collection.update_one({'_id': ObjectId(post_id)}, {'$set': post_data})
            updated_post = await post_collection.find_one({'_id': ObjectId(post_id)})
            return post_helper(updated_post)

    async def remove_post(self, post_id: str):
        post = await post_collection.find_one({'_id': ObjectId(post_id)})

        if post:
            await post_collection.delete_one({'_id': ObjectId(post_id)})
