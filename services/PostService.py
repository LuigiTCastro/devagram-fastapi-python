from models.PostModel import PostCreateModel
from providers.AWSProvider import AWSProvider
from repositories.PostRepository import PostRepository

postRepository = PostRepository()
awsProvider = AWSProvider()

class PostService:
    async def register_post(self, post: PostCreateModel, photo_path):
        try:
            new_post = await postRepository.create_post(post)

            try:
                photo_url = awsProvider.s3_file_upload(
                    photo_path,
                    f'profile-photos/{new_post["id"]}.png'
                )

                new_post = await postRepository.update_post(post['id'], {'photo': photo_url})

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