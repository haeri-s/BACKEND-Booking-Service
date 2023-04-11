from pydantic import BaseModel
from uuid import UUID

class ServiceCategoryCreateForm(BaseModel):
    category: str
    name: str


class ServiceCategory(BaseModel):
    id: int
    category: str
    name: str

    class Config:
        orm_mode = True
        

class ServiceForm(BaseModel):
    id = UUID
    category_id: int
    name: str
    price: int
    notice: str | None

    duration: int | None
    duration_unit: str | None

    is_disabled: bool = False
    is_deleted: bool = False


class Service(BaseModel):
    id = UUID
    category: ServiceCategory
    name: str
    price: int
    notice: str | None

    duration: int | None
    duration_unit: str | None

    is_disabled: bool
    is_deleted: bool

    class Config:
        orm_mode = True


