from pydantic import BaseModel
from uuid import UUID
from server.services.schemas import ServiceCategoryEnum

class ServiceCategory(BaseModel):
    id: int
    category: ServiceCategoryEnum
    name: str

    class Config:
        orm_mode = True
        
class Service(BaseModel):
    id = UUID
    name: str
    category: ServiceCategory

    class Config:
        orm_mode = True
