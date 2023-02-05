from fastapi import HTTPException, status
from pydantic import BaseModel

class CustomHTTPException(HTTPException):
    def __init__(self, status=status.HTTP_400_BAD_REQUEST, msg=None, code=None):
        self.status_code = status
        self.detail = {
            "code": code,
            "msg": msg
        }