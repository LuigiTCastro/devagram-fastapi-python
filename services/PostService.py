import os
from bson import ObjectId
from models.CommentsModel import CommentCreateModel
from models.PostModel import PostCreateModel
from providers.AWSProvider import AWSProvider
from repositories.PostRepository import PostRepository
from repositories.UserRepository import UserRepository

postRepository = PostRepository()
awsProvider = AWSProvider()
userRepository = UserRepository()


class PostService:
    async def register_post(self, post: PostCreateModel, user_id):
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
                'data': new_post,  # ??
                'status': 201
            }

        except Exception as error:
            return {
                'message': 'Internal server error.',
                'data': error,
                'status': 500
            }

    async def find_post_by_id(self, post_id: str):
        try:
            wanted_post = await postRepository.find_post_by_id(post_id)

            if wanted_post is None:
                return {
                    'message': 'Post not found.',
                    'data': '',
                    'status': 404
                }

            return {
                'message': 'Post successfully found.',
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
            posts_found = await postRepository.find_all_posts()

            if posts_found is None:
                return {
                    'message': 'Posts not found.',
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
                'data': str(error),
                'status': 500
            }

    async def list_user_posts(self, user_id: str):
        try:
            posts_found = await postRepository.find_all_user_posts(user_id)

            if not posts_found:
                return {
                    'message': 'Posts not found.',
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
                'data': str(error),
                'status': 500
            }

    async def register_like_or_dislike(self, post_id: str, user_id: str):
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

            else:
                post_found['likes'].append(ObjectId(user_id))

            post_found['total_likes'] = len(post_found['likes'])

            updated_post = await postRepository.update_post(post_found['id'], {
                'likes': post_found['likes'],
                'total_likes': post_found['total_likes']
            })

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

    async def register_comment(self, post_id: str, user_id: str, comments: str):
        try:
            post_found = await postRepository.find_post_by_id(post_id)

            if not post_found:
                return {
                    'message': 'Post not found.',
                    'data': '',
                    'status': 404
                }

            post_found['comments'].append({
                'user_id': ObjectId(user_id),
                'comments': comments
            })
            post_found['total_comments'] = len(post_found['comments'])

            updated_post = await postRepository.update_post(post_found['id'], {
                'comments': post_found['comments'],
                'total_comments': post_found['total_comments']
            })

            return {
                'message': 'Comment successfully realized.',
                'data': updated_post,
                'status': 200
            }

        except Exception as error:
            return {
                'message': 'Internal server error.',
                'data': str(error),
                'status': 500
            }

    async def remove_post_by_id(self, post_id: str, logged_user_id: str):
        try:
            post_found = await postRepository.find_post_by_id(post_id)

            if not post_found:
                return {
                    'message': 'Posts not found.',
                    'data': '',
                    'status': 404
                }

            if not post_found['user_id'] == logged_user_id:
                return {
                    'message': 'Unauthorized action.',
                    'data': '',
                    'status': 401
                }

            await postRepository.remove_post(post_id)
            return {
                'message': 'Post deleted successfully.',
                'data': '',
                'status': 200
            }

        except Exception as error:
            return {
                'message': 'Internal server error.',
                'data': str(error),
                'status': 500
            }