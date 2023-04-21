from pydantic import BaseModel, EmailStr
from uuid import UUID

class AccountBase(BaseModel):
    email: EmailStr
    name: str | None
    mobile: str | None
    role: str | None

class AccountCreateForm(AccountBase):
    password: str

class AccountUpdateForm(AccountBase):
    id: UUID

class MyInfoUpdateForm(BaseModel):
    id: UUID
    name: str 
    mobile: str | None
    role: str | None
    new_password: str | None


class Account(AccountBase):
    id: UUID

    class Config:
        orm_mode = True

class ResponseAccount(BaseModel):
    user: Account