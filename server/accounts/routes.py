from fastapi import APIRouter, Depends, HTTPException, status
from server.accounts.models import Account, AccountCreateForm, AccountUpdateForm, MyInfoUpdateForm, ResponseAccount
from server.utils.exceptions import CustomHTTPException
from server.utils.validates import validate_mobile, validate_password, validate_role
import uuid
from server.accounts.schemas import AccountDB
from server.database import create_db, get_db
from server.auth.auth import get_current_user
from sqlalchemy_utils.types.phone_number import PhoneNumberParseException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    # dependencies=[Depends(get_current_user)]
)

@router.get('/me', description='관리자 로그인 계정 정보 확인', response_model=ResponseAccount)
def get_me(user: Account = Depends(get_current_user)):
    return {'user': user}


@router.get('/', response_model=list[Account], description='관리자 계정 목록 조회')
def get_accounts(db: Session = Depends(get_db)):
    accounts = db.query(AccountDB).all()
    return accounts


@router.get('/{id}', response_model=list[Account], description='관리자 계정 상세 조회')
def get_account_detail(id, db: Session = Depends(get_db)):
    accounts = db.query(AccountDB).filter(AccountDB.id == id).one_or_none()
    return accounts

@router.post('/', description='관리자 계정 생성', response_model=Account)
def create_account(form_data: AccountCreateForm, db:Session=Depends(get_db)):
    try:
        data = {"id":uuid.uuid4(), **form_data.dict()}
        validate_mobile(data.get('mobile'))
        validate_password(data.get('password'))
        result = AccountDB(**data)
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

@router.put('/', description='관리자 계정 정보 수정 생성', response_model=ResponseAccount)
def create_account(form_data: AccountUpdateForm, db:Session=Depends(get_db)):
    try:
        validate_mobile(form_data.mobile)

        account = db.query(AccountDB).filter(AccountDB.id == form_data.id).one_or_none()
        if not account:
            raise CustomHTTPException(msg="사용자 정보가 맞지 않습니다.", code="NOT_FOUND_MANAGER")
        account.name = form_data.name
        account.email = form_data.email
        account.mobile = form_data.mobile
        db.add(account)
        db.commit()
        db.refresh(account)
        return {'user': account}
    except CustomHTTPException as e:
        raise e
    except PhoneNumberParseException :
        raise CustomHTTPException(msg="휴대폰 번호를 다시 확인해주세요.", code="PHONE_NUMBER_INVALID")
    except Exception as err:
        if 'already exists' in err.__str__():
            raise CustomHTTPException(msg="이미 가입되어 있는 이메일입니다.", code="EMAIL_ALREADY_USED")
        raise CustomHTTPException(msg=err.__str__())

@router.put('/me', description='본인 계정 정보 수정 생성', response_model=ResponseAccount)
def update_account(form_data: MyInfoUpdateForm, current_user: AccountDB = Depends(get_current_user), db:Session=Depends(get_db)):
    try:
        account = db.query(AccountDB).filter(AccountDB.id == current_user.id).one_or_none()
        if not account:
            raise CustomHTTPException(msg="사용자 정보가 맞지 않습니다.", code="NOT_FOUND_MANAGER")

        validate_mobile(form_data.mobile)
        if form_data.new_password and len(form_data.new_password):
            validate_password(form_data.new_password)
            account.password = form_data.new_password
        
        validate_role(form_data.role)

        account.name = form_data.name
        account.mobile = form_data.mobile
        account.role = form_data.role
        db.add(account)
        db.commit()
        db.refresh(account)

        return {'user': account}
    except CustomHTTPException as e:
        raise e
    except PhoneNumberParseException :
        raise CustomHTTPException(msg="휴대폰 번호를 다시 확인해주세요.", code="PHONE_NUMBER_INVALID")
    except Exception as err:
        if 'already exists' in err.__str__():
            raise CustomHTTPException(msg="이미 가입되어 있는 이메일입니다.", code="EMAIL_ALREADY_USED")
        raise CustomHTTPException(msg=err.__str__())

