from server.utils.exceptions import CustomHTTPException
import re
from sqlalchemy_utils.types.phone_number import PhoneNumberParseException


def validate_password(pwd):
    if len(pwd) < 6:
        raise CustomHTTPException(msg="비밀번호로 6자 이상의 글자를 입력해주세요", code="INVALID_PASSWORD")
    return True

def validate_mobile(mobile):
    if len(mobile) > 12:
        raise PhoneNumberParseException(-1, '잘못된 휴대폰 번호 입력')
    com = re.compile('^01[0-9]+')
    tmp = com.match(mobile)
    if (not tmp) or mobile != tmp.group():
        raise PhoneNumberParseException(-1, '잘못된 휴대폰 번호 입력')
    return True

def validate_role(role):
    if not role in ['all', 'manager', 'staff']:
        raise CustomHTTPException(msg="권한이 잘못되었습니다", code="INVALID_ROLE")
    return True