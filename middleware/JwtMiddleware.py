from utils.JwtToken import JwtToken
from fastapi import HTTPException, Header


class JwtMiddleware:

    async def verify_token(authorization: str = Header(default='')):
        if not authorization.split(' ')[0] == 'Bearer':
            raise HTTPException(status_code=401, detail='Its necessary to provide a token.')

        token = authorization.split(' ')[1]
        payload = JwtToken.decode_jwt_token(token)

        if not payload:
            raise HTTPException(status_code=401, detail='Invalid token.')

        return payload
