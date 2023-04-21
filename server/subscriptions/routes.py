from fastapi import APIRouter, Depends
import server.auth.auth
from server.subscriptions.schemas import UserDB, UserSubscribeDB
from server.subscriptions.models import (Subscription, SubscriptionDeleteForm, SubscriptionForm,
    SubscriptionWithUser, User)
from sqlalchemy.orm import Session
from server.database import create_db, get_db
from server.auth.auth import get_current_user
from server.utils.validates import validate_password, validate_mobile
from server.utils.exceptions import CustomHTTPException
from sqlalchemy_utils.types.phone_number import PhoneNumberParseException
import uuid
from server.accounts.models import Account
from server.utils.models import StatusModel

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get('/', response_model=list[SubscriptionWithUser], description='구독한 계정 목록 조회')
def get_subscriptions(db: Session = Depends(get_db), 
    # current_user: Account = Depends(get_current_user)
):
    subscriptions = db.query(UserSubscribeDB).all()
    return subscriptions

@router.post('/', description='마케팅 구독 정보 생성 및 수정', response_model=User)
def create_subscription(form_data: SubscriptionForm, db:Session=Depends(get_db)):
    try:
        data = {"id":uuid.uuid4(), **form_data.dict()}
        is_marketing = data.pop('is_marketing')
        mobile = data.get('mobile')
        if mobile:
            validate_mobile(data.get('mobile'))

        # 구독 이력 조회
        old = db.query(UserDB).filter(UserDB.email==data.get('email')).one_or_none()
        if not old:
            # 구독 이력 없는 경우
            user = UserDB(**data)
            db.add(user)
            if is_marketing:
                db.add(UserSubscribeDB(user_id=user.id))
        else:
            user = old
            # 구독 이력 있는 경우 - 이름, 모바일, 모바일 국가코드, 정보 갱신
            if data.get('name'):
                user.name = data.get('name')
            if mobile:
                user.mobile = data.get('mobile')
                user.mobile_country_code = data.get('mobile_country_code')
            
            db.add(user)
            # 구독 여부가 이전과 다른 경우 확인
            if is_marketing != len(user.subscribes):
                # 구독 신청한 경우
                if is_marketing:
                    db.add(UserSubscribeDB(user_id=user.id))
                # 구독 취소한 경우
                else:
                    for s in user.subscribes:
                        db.delete(s)
        db.commit()
        db.refresh(user)

        return user
    except CustomHTTPException as e:
        raise e
    except PhoneNumberParseException :
        raise CustomHTTPException(msg="휴대폰 번호를 다시 확인해주세요.", code="PHONE_NUMBER_INVALID")
    except Exception as err:
        if 'already exists' in err.__str__():
            raise CustomHTTPException(msg="이미 가입되어 있는 이메일입니다.", code="EMAIL_ALREADY_USED")
        raise CustomHTTPException(msg=err.__str__())


@router.delete('/subscribe', description='마케팅 구독 정보 수정', response_model=StatusModel)
def delete_subscription(form_data: SubscriptionDeleteForm, db:Session=Depends(get_db)):
    try:
        # 구독 이력 조회
        user = db.query(UserDB).filter(UserDB.email==form_data.email).one_or_none()
        if user:
            if user.subscribes and len(user.subscribes):
                for s in user.subscribes:
                    db.delete(s)
                db.commit()
                db.refresh(user)

        return StatusModel()
    except Exception as err:
        raise CustomHTTPException(msg=err.__str__())
