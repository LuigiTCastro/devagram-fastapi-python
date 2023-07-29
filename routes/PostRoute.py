import os

from fastapi import APIRouter, UploadFile, HTTPException, Depends, File
from models.PostModel import PostCreateModel
from services.PostService import PostService

postService = PostService()
router = APIRouter()


class PostRoute:

    @router.post('/register', response_description='Route that creates a new publish.')
    async def register_post(self, file: UploadFile = File(...), post: PostCreateModel = Depends(PostCreateModel)):
        try:
            print(file.filename)
            photo_path = f'file/{file.filename}.png'

            with open(photo_path, 'wb+') as file:
                file.write(file.read())

            result = await postService.register_post(post, photo_path)
            os.remove(photo_path)

            if not result['status'] == 201:
                raise HTTPException(status_code=result['status'], detail=result['message'])

            return result

        except Exception as error:
            print(error)

    @router.get('/get', response_description='...')
    async def get_post(self):
        pass
