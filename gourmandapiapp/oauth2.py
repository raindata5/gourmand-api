from datetime import datetime, timedelta
from fastapi.param_functions import Depends
from jose import jwt
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    HTTPBasic,
    HTTPBasicCredentials
)
import secrets
from jose.exceptions import JWTError
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import user
from . import models
from .db import get_db
from . import schemas, utils
from fastapi import HTTPException, status, Cookie
from gourmandapiapp.config import settings
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBasic()

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


# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
# test for cookie-based auth instead of oauth2
def get_current_user(Authorization: Annotated[str, Cookie()] , db: Session = Depends(get_db)):
    token = Authorization.split(' ')[1]
    print(token)
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_data = verify_access_token(token, credentials_exception)
    user_obj = db.query(models.AuthUserModelORM).filter(models.AuthUserModelORM.userid == token_data.userid).first()
    return user_obj

def verify_email_and_pass(current_email, current_password, correct_user, correct_pass):
    current_email_bytes = current_email
    correct_email_bytes = correct_user

    is_correct_email = secrets.compare_digest(
        current_email_bytes, correct_email_bytes
    )


    # current_password_hash = utils.get_password_hash(current_password)
    current_password_hash = current_password

    correct_password_hash = correct_pass

    is_correct_password = utils.verification(
        current_password_hash,
        correct_password_hash
    )

    # is_correct_password = secrets.compare_digest(
    #     current_password_hash, correct_password_hash
    # )
    return is_correct_email and is_correct_password


# def get_current_user_simple(
#     credentials: Annotated[HTTPBasicCredentials, Depends(security)],
#     db: Session = Depends(get_db)
# ):
#     user_obj = db.query(models.AuthUserModelORM).filter(models.AuthUserModelORM.email == credentials.email).first()

#     current_email_bytes = credentials.username.encode("utf8")
#     correct_email_bytes = user_obj.email

#     is_correct_email = secrets.compare_digest(
#         current_email_bytes, correct_email_bytes
#     )


#     current_password_hash = utils.get_password_hash(credentials.password)

#     correct_password_hash = user_obj.password

#     is_correct_password = secrets.compare_digest(
#         current_password_hash, correct_password_hash
#     )
#     credentials_exception = HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
    # token_data = verify_access_token(token, credentials_exception)
    # return user_obj
    # return is_correct_email and is_correct_password