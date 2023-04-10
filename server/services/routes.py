from fastapi import APIRouter, Depends, HTTPException, status
from server.services.models import Service, ServiceCategory
from server.utils.exceptions import CustomHTTPException
from server.utils.validates import validate_password, validate_mobile
import uuid
from server.services.schemas import ServiceDB, ServiceCategoryDB
from server.database import create_db, get_db
from server.auth.auth import get_current_user
from sqlalchemy_utils.types.phone_number import PhoneNumberParseException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/services",
    tags=["services"],
    # dependencies=[Depends(get_current_user)]
)

@router.get('/categories', response_model=list[ServiceCategory], description='서비스 유형 목록 조회')
def get_managers(db: Session = Depends(get_db)):
    services = db.query(ServiceCategoryDB).all()
    print(services)
    return services

@router.get('/', response_model=list[Service], description='서비스 목록 조회')
def get_managers(db: Session = Depends(get_db)):
    services = db.query(ServiceDB).all()
    return services