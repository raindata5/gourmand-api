from datetime import datetime, timedelta
from fastapi.param_functions import Depends
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose.exceptions import JWTError
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import user
from . import models
from .db import get_db
from . import schemas
from fastapi import HTTPException, status
from gourmandapiapp.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(user_data: dict ):
    to_encode = user_data.copy()
    token_expiration = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": token_expiration})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    
        userid: str = payload.get("userid")
        if not userid:
            raise credentials_exception             
        token_data = schemas.TokenData(userid=userid)
    except JWTError as e:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_data = verify_access_token(token, credentials_exception)
    user_obj = db.query(models.AuthUserModelORM).filter(models.AuthUserModelORM.userid == token_data.userid).first()
    return user_obj