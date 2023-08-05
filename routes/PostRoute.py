from fastapi import APIRouter, UploadFile, HTTPException, Depends, File, Header
from middleware.JwtMiddleware import JwtMiddleware
from models.PostModel import PostCreateModel
from services.AuthService import AuthService
from services.PostService import PostService
from services.UserService import UserService
from utils.JwtToken import JwtToken

postService = PostService()
userService = UserService()
authService = AuthService()
jwtToken = JwtToken()
router = APIRouter()


@router.post(
    '/register',
    response_description='Route responsible for creating a new publish.',
    dependencies=[Depends(JwtMiddleware.verify_token)]
)
async def register_post(
        authorization: str = Header(default=''),
        post: PostCreateModel = Depends(PostCreateModel)
):
    try:
        logged_user = await authService.get_logged_user(authorization)
        result = await postService.register_post(post, logged_user['id'])

        if not result['status'] == 201:
            raise HTTPException(status_code=result['status'], detail=result['message'])

        return result

    except Exception as error:
        print(error)


@router.get(
    '/get/{post_id}',
    response_description='Route responsible for obtaining the data of a publish through the id.',
    dependencies=[Depends(JwtMiddleware.verify_token)]
)
async def get_post_info(post_id: str):
    try:
        result = await postService.find_post_by_id(post_id)

        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'], detail=result['message'])

        return result

    except Exception as error:
        raise error


@router.get(
    '/list',
    response_description='Route responsible for listing all posts of the database.',
    dependencies=[Depends(JwtMiddleware.verify_token)]
)
async def get_posts_list():
    try:
        result = await postService.list_posts()

        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'], detail=result['message'])

        return result

    except Exception as error:
        raise error


@router.put(
    '/like/{post_id}',
    response_description='Responsible route to like/dislike a post.',
    dependencies=[Depends(JwtMiddleware.verify_token)]
)
async def post_like_or_dislike(post_id: str, authorization: str = Header(default='')):
    try:
        logged_user = await authService.get_logged_user(authorization)
        result = await postService.register_like_or_dislike(post_id, logged_user['id'])

        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'], detail=result['message'])

        return result

    except Exception as error:
        raise error
