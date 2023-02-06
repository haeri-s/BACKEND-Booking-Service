from fastapi import APIRouter, Depends
from server.subscriptions.schemas import SubscriptionDB
from server.subscriptions.models import Subscription, SubscriptionBase
from sqlalchemy.orm import Session
from server.database import create_db, get_db
from server.utils.validates import validate_password, validate_mobile
from server.utils.exceptions import CustomHTTPException
from sqlalchemy_utils.types.phone_number import PhoneNumberParseException
import uuid

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
)


@router.get('/', response_model=list[Subscription], description='구독자 계정 목록 조회')
def get_subscriptions(db: Session = Depends(get_db)):
    subscriptions = db.query(SubscriptionDB).all()
    return subscriptions

@router.post('/', description='마케팅 구독 정보 생성', response_model=Subscription)
def create_Subscription(form_data: SubscriptionBase, db:Session=Depends(get_db)):
    try:
        data = {"id":uuid.uuid4(), **form_data.dict()}
        validate_mobile(data.get('mobile'))
        validate_password(data.get('password'))
        result = SubscriptionDB(**data)
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
