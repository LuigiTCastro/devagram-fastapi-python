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
    response_description='Route that creates a new publish.',
    dependencies=[Depends(JwtMiddleware.verify_token)]
)
# async def register_post(file: UploadFile = File(...), post: PostCreateModel = Depends(PostCreateModel)):
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


@router.get('/get', response_description='...', dependencies=[Depends(JwtMiddleware.verify_token)])
# async def get_post(authorization: str = Header(default='')):
async def get_post(id: str):
    try:
        # token = authorization.split(' ')[1]
        # payload = jwtToken.decode_jwt_token(token)
        # logged_user = await userService.find_user_by_id(payload['user_id'])\

        result = await postService.find_post_by_id(id)

        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'], detail=result['message'])

        return result

    except Exception as error:
        raise error


@router.get('/list', response_description='...', dependencies=[Depends(JwtMiddleware.verify_token)])
async def get_posts():
    try:
        result = await postService.list_posts()

        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'], detail=result['message'])

        return result

    except Exception as error:
        raise error
