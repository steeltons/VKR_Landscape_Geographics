from fastapi import HTTPException, status

class JwtUnauthorizedException(HTTPException):

    def __init__(self, message: str = 'Invalid authentication credentials'):
        super().__init__(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= message,
            headers={'WWW-Authenticate' : 'Bearer'}
        )