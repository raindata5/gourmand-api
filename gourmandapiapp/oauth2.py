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
from fastapi import HTTPException, status, Cookie, Request
from gourmandapiapp.config import settings
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBasic()

TOKEN_ARGS = {
    "access_token_general": {
        "remember_me_minutes_offset": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 2,
        "expiration_offset_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    } ,
    "verification_token_general": {
        "expiration_offset_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES
    } ,
}

def create_access_token(user_data: dict, token_type: str = 'access_token_general' ):
    to_encode = user_data.copy()
    minutes_offset=TOKEN_ARGS[token_type]["expiration_offset_minutes"]
    if to_encode.get("remember_me", False):
        minutes_offset=TOKEN_ARGS[token_type]["remember_me_minutes_offset"]

    token_expiration = datetime.utcnow() + timedelta(minutes=minutes_offset)
    to_encode.update({"exp": token_expiration})
    if token_type == "access_token_general":
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    elif token_type == "verification_token_general":
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception, strict=True):
    userid = None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    
        userid: str = payload.get("userid")
        token_data = schemas.TokenData(userid=userid)

    except JWTError as e:
        print(f"{userid} and {strict}")
        if not userid and strict:
            raise credentials_exception     
        elif not userid and strict == False:
            return None
    return token_data


# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
# test for cookie-based auth instead of oauth2
def get_current_user_lax(Authorization: Annotated[str, Cookie()] = 'Bearer default' , db: Session = Depends(get_db)):
    token = Authorization.split(' ')[1]
    token_data = verify_access_token(token, credentials_exception=None, strict=False)

    if not token_data:
        return models.AuthUserModelORM(userid="Guest")


    user_obj = db.query(models.AuthUserModelORM).filter(models.AuthUserModelORM.userid == token_data.userid).first()
    return user_obj

def get_current_user_strict(request: Request, Authorization: Annotated[str, Cookie()] = 'Bearer default', db: Session = Depends(get_db)):
    token = Authorization.split(' ')[1]
    # print(request.url.path)
    # print(request.scope)
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer",},
        )
    token_data = verify_access_token(token, credentials_exception)
    user_obj = db.query(models.AuthUserModelORM).filter(models.AuthUserModelORM.userid == token_data.userid).first()
    return user_obj

def verify_email_and_pass(current_email, current_password, correct_user, correct_pass):
    current_email_bytes = bytes(current_email, 'utf-8')
    correct_email_bytes = bytes(correct_user, 'utf-8')

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