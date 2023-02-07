from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str | None
    mobile: str | None
    mobile_country_code: str = '82'

class SubscriptionForm(UserBase):
    is_marketing: bool = False

class SubscriptionDeleteForm(BaseModel):
    email: EmailStr

class SubsciptionUser(UserBase):
    id: UUID

    class Config:
        orm_mode = True

class SubscriptionWithUser(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime | None
    user: SubsciptionUser

    class Config:
        orm_mode = True

class Subscription(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True

class User(UserBase):
    id: UUID
    subscribes: list[Subscription] | None

    class Config:
        orm_mode = True
    