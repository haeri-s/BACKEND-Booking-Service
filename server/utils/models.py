from pydantic import BaseModel


class StatusModel(BaseModel):
    status: str = 'success'