from fastapi import HTTPException, status
from pydantic import BaseModel

class CustomHTTPException(HTTPException):
    def __init__(self, status=status.HTTP_400_BAD_REQUEST, msg=None, code=None):
        self.status_code = status
        self.detail = {
            "code": code,
            "msg": msg
        }

class ValidationException(CustomHTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = {
            'code': 'is_not_valid',
            'msg': '데이터를 확인해주세요'
        }