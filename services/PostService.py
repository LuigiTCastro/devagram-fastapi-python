import os

from bson import ObjectId

from models.PostModel import PostCreateModel
from providers.AWSProvider import AWSProvider
from repositories.PostRepository import PostRepository

postRepository = PostRepository()
awsProvider = AWSProvider()


class PostService:
    async def register_post(self, post: PostCreateModel, user_id):
        # async def register_post(self, post: PostCreateModel):
        try:
            created_post = await postRepository.create_post(post, user_id)
            # photo_upload = created_post.photo
            photo_upload = post.photo

            try:
                photo_path = f'file/{photo_upload.filename}.png'

                with open(photo_path, 'wb+') as f:
                    f.write(photo_upload.file.read())

                photo_url = awsProvider.s3_file_upload(
                    photo_path,
                    f'publish-photos/{created_post["id"]}.png'
                )

                new_post = await postRepository.update_post(created_post['id'], {'photo': photo_url})
                os.remove(photo_path)

            except Exception as error:
                print(error)

            return {
                'message': 'Post successfully realized.',
                'data': new_post,
                'status': 201
            }

        except Exception as error:
            return {
                'message': 'Internal server error.',
                'data': error,
                'status': 500
            }

    async def find_post_by_id(self, id: str):
        try:
            wanted_post = await postRepository.find_post_by_id(id)

            if wanted_post is None:
                return {
                    'message': 'Post not found.',
                    'data': '',
                    'status': 404
                }

            return {
                'message': '',
                'data': wanted_post,
                'status': 200
            }

        except Exception as error:
            return {
                'message': 'Internal server error.',
                'data': error,
                'status': 500
            }

    async def list_posts(self):
        try:
            posts_found = await postRepository.find_posts()

            for p in posts_found:
                p.total_likes = len(p.likes)

            return {
                'message': 'Posts successfully listed.',
                'data': posts_found,
                'status': 200
            }

        except Exception as error:
            return {
                'message': 'Internal server error.',
                'data': str(error),
                'status': 500
            }

    async def register_like(self, post_id: str, user_id: str):
        try:
            post_found = await postRepository.find_post_by_id(post_id)

            if not post_found:
                return {
                    'message': 'Post not found.',
                    'data': '',
                    'status': 404
                }

            if post_found['likes'].count(user_id) > 0:
                post_found['likes'].remove(user_id)
                post_found['total_likes'] = len(post_found['likes'])
            else:
                post_found['likes'].append(ObjectId(user_id))
                post_found['total_likes'] = len(post_found['likes'])

            updated_post = await postRepository.update_post(post_found['id'],
                                                            {'likes': post_found['likes'],
                                                             'total_likes': post_found['total_likes']})

            if updated_post['likes'].count(user_id) > 0:
                return {
                    'message': f'The post was LIKED successfully.',
                    'data': updated_post,
                    'status': 200
                }
            else:
                return {
                    'message': f'The post was DISLIKED successfully.',
                    'data': updated_post,
                    'status': 200
                }

        except Exception as error:
            return {
                'message': 'Internal server error.',
                'data': str(error),
                'status': 500
            }
