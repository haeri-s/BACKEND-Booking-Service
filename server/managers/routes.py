from fastapi import APIRouter, Depends, HTTPException, status
from server.managers.models import Manager, ManagerForm
from server.utils import CustomHTTPException
import uuid
from server.managers.schemas import ManagerDB
from server.database import create_db, get_db
from ..auth.auth import get_current_user
from sqlalchemy_utils.types.phone_number import PhoneNumberParseException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/managers",
    tags=["managers"],
    dependencies=[Depends(get_current_user)]
)

def validate_password(pwd):
    if len(pwd) < 6:
        raise CustomHTTPException(msg="비밀번호로 6자 이상의 글자를 입력해주세요.", code="INVALID_PASSWORD")
    return
    
@router.post('/', description='관리자 계정 생성', response_model=Manager)
def create_manager(manager: ManagerForm, db:Session=Depends(get_db)):
    try:
        data = {"id":uuid.uuid4(), **manager.dict()}
        validate_password(data.get('password'))
        result = ManagerDB(**data)
        result = create_db(db, result)
    except PhoneNumberParseException :
        raise CustomHTTPException(msg="휴대폰 번호를 다시 확인해주세요.", code="PHONE_NUMBER_INVALID")
    except Exception as err:
        if 'already exists' in err.__str__():
            raise CustomHTTPException(msg="이미 가입되어 있는 이메일입니다.", code="EMAIL_ALREADY_USED")
        raise CustomHTTPException(msg=err.__str__())
    return data

@router.get('/me', description='관리자 로그인 계정 정보 확인', response_model=Manager)
def create_manager(user: Manager = Depends(get_current_user)):
    return user


@router.get('/', response_model=list[Manager], description='관리자 계정 목록 조회')
def get_managers(db: Session = Depends(get_db)):
    managers = db.query(ManagerDB).all()
    return managers