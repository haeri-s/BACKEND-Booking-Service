from pydantic import BaseModel, EmailStr
from server.accounts.models import Account
from datetime import datetime

class Token(BaseModel):
    accessToken: str
    expire: datetime
    tokenType: str = 'bearer'

class TokenData(BaseModel):
    email: EmailStr
    mobile: str

class LoginForm(BaseModel):
    username: EmailStr
    password: str
    # grant_type: str | None

class LoginToken(Token):
    user: Account