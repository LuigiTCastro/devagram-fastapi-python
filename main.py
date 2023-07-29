from fastapi import FastAPI

from routes.UserRoute import router as UserRoute
from routes.AuthRoute import router as AuthRoute
from routes.PostRoute import router as PostRoute
from test_route import router as test_route

app = FastAPI()

app.include_router(UserRoute, tags=['User'], prefix='/api/user')
app.include_router(AuthRoute, tags=['Auth'], prefix='/api/auth')
app.include_router(PostRoute, tags=['Post'], prefix='/api/post')
app.include_router(test_route, tags=['Test'], prefix='/api/test')
