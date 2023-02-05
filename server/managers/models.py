from pydantic import BaseModel, EmailStr
import sqlalchemy_utils
from uuid import UUID

class ManagerBase(BaseModel):
    email: EmailStr
    name: str | None
    mobile: str | None


class ManagerForm(ManagerBase):
    password: str

class Manager(ManagerBase):
    id: UUID

    class Config:
        orm_mode = True
        