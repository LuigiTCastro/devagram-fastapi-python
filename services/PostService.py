import os

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

            if posts_found is None:
                return {
                    'message': 'Post not found.',
                    'data': '',
                    'status': 404
                }

            return {
                'message': 'Posts successfully listed.',
                'data': posts_found,
                'status': 200
            }

        except Exception as error:
            return {
                'message': 'Internal server error.',
                'data': error,
                'status': 500
            }
