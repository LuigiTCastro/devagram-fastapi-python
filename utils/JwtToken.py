import os
import time
import jwt
from fastapi import Depends, HTTPException, FastAPI
from decouple import config

app = FastAPI()

SECRET_KEY = config("SECRET_KEY")
# SECRET_KEY = os.getenv("SECRET_KEY", "MY-SECRET-KEY")
ALGORITHM = "HS256"


class JwtToken:
    def generate_jwt_token(self, user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "expires": time.time() + 6000
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token

    def decode_jwt_token(self, token: str):
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

            if decoded_token['expires'] >= time.time():
                return decoded_token
            else:
                return None

        except Exception as error:
            print(error)
            return None

    def get_current_user(token: str = Depends(jwt.decode)) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            user_id = payload.get('user_id')

            if user_id is None:
                raise HTTPException(status_code=401, detail='Invalid token.')

            user = {'id': user_id, 'username': 'example'}
            return user

        except jwt.PyJWTError:  # JWTError?
            raise HTTPException(status_code=401, detail='Invalid token.')

    # @app.get("/protected_route")
    # async def protected_route(user: dict = Depends(get_current_user)):
    #     return {"message": f"Hello, {user['username']}. This is a protected route."}

