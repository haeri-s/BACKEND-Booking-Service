from datetime import datetime, timedelta
from fastapi import Header, HTTPException
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from server.config import get_settings
from server.auth.models import LoginForm, TokenData
from sqlalchemy.orm import Session
from server.database import get_db
from server.accounts.schemas import AccountDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

settings = get_settings()
jwt_setting = settings.jwt_setting
secret_key = jwt_setting.get('secret_key')
algorithm = jwt_setting.get('algorithm')


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(days=jwt_setting.get('expire_days'))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return {'accessToken': encoded_jwt, 'expire': expire}

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    x_token = token
    print(x_token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"x_token": ""},
    )
    
    try:
        payload = jwt.decode(x_token, secret_key, algorithms=[algorithm])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        print(JWTError)
        raise credentials_exception
    user = db.query(AccountDB).filter(AccountDB.email == email).one_or_none()
    if not user:
        raise credentials_exception
    return user

