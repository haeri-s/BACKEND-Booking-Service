from pydantic import BaseModel, EmailStr
from uuid import UUID

class ManagerBase(BaseModel):
    email: EmailStr
    name: str | None
    mobile: str | None

class ManagerCreateForm(ManagerBase):
    password: str

class ManagerUpdateForm(ManagerBase):
    id: UUID

class MyInfoUpdateForm(ManagerBase):
    new_password: str | None


class Manager(ManagerBase):
    id: UUID

    class Config:
        orm_mode = True
