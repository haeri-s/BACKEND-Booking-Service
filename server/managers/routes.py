from fastapi import APIRouter, Depends, HTTPException, status
from server.managers.models import Manager, ManagerCreateForm, ManagerUpdateForm, MyInfoUpdateForm
from server.utils.exceptions import CustomHTTPException
from server.utils.validates import validate_password, validate_mobile
import uuid
from server.managers.schemas import ManagerDB
from server.database import create_db, get_db
from server.auth.auth import get_current_user
from sqlalchemy_utils.types.phone_number import PhoneNumberParseException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/managers",
    tags=["managers"],
    # dependencies=[Depends(get_current_user)]
)

@router.get('/me', description='관리자 로그인 계정 정보 확인', response_model=Manager)
def get_me(user: Manager = Depends(get_current_user)):
    return user


@router.get('/', response_model=list[Manager], description='관리자 계정 목록 조회')
def get_managers(db: Session = Depends(get_db)):
    managers = db.query(ManagerDB).all()
    return managers

@router.post('/', description='관리자 계정 생성', response_model=Manager)
def create_manager(form_data: ManagerCreateForm, db:Session=Depends(get_db)):
    try:
        data = {"id":uuid.uuid4(), **form_data.dict()}
        validate_mobile(data.get('mobile'))
        validate_password(data.get('password'))
        result = ManagerDB(**data)
        result = create_db(db, result)
    except CustomHTTPException as e:
        raise e
    except PhoneNumberParseException :
        raise CustomHTTPException(msg="휴대폰 번호를 다시 확인해주세요.", code="PHONE_NUMBER_INVALID")
    except Exception as err:
        if 'already exists' in err.__str__():
            raise CustomHTTPException(msg="이미 가입되어 있는 이메일입니다.", code="EMAIL_ALREADY_USED")
        raise CustomHTTPException(msg=err.__str__())
    return data

@router.put('/', description='관리자 계정 정보 수정 생성', response_model=Manager)
def create_manager(form_data: ManagerUpdateForm, db:Session=Depends(get_db)):
    try:
        validate_mobile(form_data.mobile)

        manager = db.query(ManagerDB).filter(ManagerDB.id == form_data.id).one_or_none()
        if not manager:
            raise CustomHTTPException(msg="사용자 정보가 맞지 않습니다.", code="NOT_FOUND_MANAGER")
        manager.name = form_data.name
        manager.email = form_data.email
        manager.mobile = form_data.mobile
        db.add(manager)
        db.commit()
        db.refresh(manager)
        return manager
    except CustomHTTPException as e:
        raise e
    except PhoneNumberParseException :
        raise CustomHTTPException(msg="휴대폰 번호를 다시 확인해주세요.", code="PHONE_NUMBER_INVALID")
    except Exception as err:
        if 'already exists' in err.__str__():
            raise CustomHTTPException(msg="이미 가입되어 있는 이메일입니다.", code="EMAIL_ALREADY_USED")
        raise CustomHTTPException(msg=err.__str__())

@router.put('/me', description='본인 계정 정보 수정 생성', response_model=Manager)
def create_manager(form_data: MyInfoUpdateForm, current_user: ManagerDB = Depends(get_current_user), db:Session=Depends(get_db)):
    try:
        manager = db.query(ManagerDB).filter(ManagerDB.id == current_user.id).one_or_none()
        if not manager:
            raise CustomHTTPException(msg="사용자 정보가 맞지 않습니다.", code="NOT_FOUND_MANAGER")

        validate_mobile(form_data.mobile)
        if form_data.new_password and len(form_data.new_password):
            validate_password(form_data.new_password)
            manager.password = form_data.new_password
        
        manager.name = form_data.name
        manager.email = form_data.email
        manager.mobile = form_data.mobile
        db.add(manager)
        db.commit()
        db.refresh(manager)
        return manager
    except CustomHTTPException as e:
        raise e
    except PhoneNumberParseException :
        raise CustomHTTPException(msg="휴대폰 번호를 다시 확인해주세요.", code="PHONE_NUMBER_INVALID")
    except Exception as err:
        if 'already exists' in err.__str__():
            raise CustomHTTPException(msg="이미 가입되어 있는 이메일입니다.", code="EMAIL_ALREADY_USED")
        raise CustomHTTPException(msg=err.__str__())

