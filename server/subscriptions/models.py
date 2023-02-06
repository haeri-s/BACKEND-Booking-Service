from pydantic import BaseModel, EmailStr
from uuid import UUID

class SubscriptionBase(BaseModel):
    email: EmailStr
    name: str | None
    mobile: str | None
    mobile_contry_code: str = '82'
    is_marketing: bool = False

class SubscriptionDeleteForm(BaseModel):
    id: UUID
    is_deleted: bool = False

class Subscription(SubscriptionBase):
    id: UUID

    class Config:
        orm_mode = True