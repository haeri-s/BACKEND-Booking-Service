from fastapi import APIRouter, Depends, HTTPException, status
from server.services.models import Service, ServiceCategory, ServiceCategoryCreateForm, ServiceForm
from server.utils.exceptions import CustomHTTPException, ValidationException
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

@router.post('/categories', response_model=ServiceCategory, description='서비스 유형 생성')
def create_category(form_data: ServiceCategoryCreateForm, db: Session = Depends(get_db)):
    try:
        if form_data.category not in ['training', 'fun', 'discovery', 'specialty']:
            raise ValidationException()
        result = create_db(db, ServiceCategoryDB(**form_data.dict()))
        return result
    except CustomHTTPException as e:
        raise e
    except Exception as err:
        raise CustomHTTPException(msg=err.__str__())

@router.get('/categories', response_model=list[ServiceCategory], description='서비스 유형 목록 조회')
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(ServiceCategoryDB).all()
    print(categories)
    return categories

@router.post('/', response_model=Service, description='서비스 생성')
def create_service(form_data: ServiceForm, db: Session = Depends(get_db)):
    try:
        data = {"id":uuid.uuid4(), **form_data.dict()}
        result = create_db(db, ServiceDB(**data))
        return result
    except CustomHTTPException as e:
        raise e
    except Exception as err:
        raise CustomHTTPException(msg=err.__str__())


@router.get('/', response_model=list[Service], description='서비스 목록 조회')
def get_services(db: Session = Depends(get_db)):
    services = db.query(ServiceDB).all()
    return services