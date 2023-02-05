from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from ..auth.dependencies import get_token_header

router = APIRouter(
  prefix="/users",
  tags=["items"],
  dependencies=[Depends(get_token_header)]
)

@router.get('/')
def get_users():
    print('usersss')
    return
# jwt.