from pydantic import BaseModel, EmailStr
from server.managers.models import Manager
from datetime import datetime

class Token(BaseModel):
    access_token: str
    expire: datetime
    token_type: str = 'bearer'

class TokenData(BaseModel):
    email: EmailStr
    mobile: str

class LoginForm(BaseModel):
    username: EmailStr
    password: str
    grant_type: str | None

class LoginToken(Token):
    user: Manager