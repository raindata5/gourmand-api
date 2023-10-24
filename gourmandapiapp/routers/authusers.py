from sqlalchemy.orm import Session
from gourmandapiapp import models, schemas, utils, oauth2
from ..db import get_db
from sqlalchemy.sql.expression import text
from sqlalchemy import desc
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Request,
    Form,
    Response
)
from pydantic import EmailStr
from fastapi.templating import Jinja2Templates
from typing import (
    Optional,
    Annotated
)
import logging
from fastapi.responses import RedirectResponse

# logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

templates = Jinja2Templates(directory="gourmandapiapp/templates")
router = APIRouter(prefix= '/auth',
                    tags=['authusers'])


@router.get('/register')
def get_create_user(request: Request, user_obj: models.AuthUserModelORM = Depends(oauth2.get_current_user_lax)):
    return templates.TemplateResponse(
        "auth_register.html",
        context={
            "request": request,
            "user_obj": user_obj,
        }
    )
@router.post('/register', status_code=status.HTTP_201_CREATED)
async def create_user(
    request: Request,
    email_input: Annotated[EmailStr, Form(min_length=1, max_length=64)],
    password_input: Annotated[str, Form(description='Passwords must match.')],
    password_input_2: Annotated[str, Form(description='Confirm password')],
    db: Session = Depends(get_db)
):
    user_data_dict = {
        "email_input": email_input,
        "password_input": password_input,
        "password_input_2": password_input_2,
    }
    user_data = schemas.CreateNewUserSchema(**user_data_dict)
    fetched_user = db.query(models.AuthUserModelORM).filter(models.AuthUserModelORM.email == user_data.email_input).first()
    if fetched_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="This email is already taken.")
    elif user_data.password_input != user_data.password_input_2:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="The passwords provided do not match.")
    password_input_hash = utils.get_password_hash(user_data.password_input)
    user_obj_new = models.AuthUserModelORM(
        email=user_data.email_input,
        password=password_input_hash
    )
    db.add(user_obj_new)
    db.commit()
    db.refresh(user_obj_new)
    
    verification_token = oauth2.create_token(
        user_data= {"userid": user_obj_new.userid},
        token_type="verification_token_general"
    ) 
    token_data = oauth2.verify_token(verification_token, credentials_exception=None)
    logging.info(f"Sending email to {user_obj_new.email} \n with the token: {verification_token} containing the userid: {token_data.userid} matched to userid: {user_obj_new.userid}")
    logging.info(f"Confirmation url: {request.url.path} or {request.base_url}auth/verify/{verification_token}")
    return RedirectResponse(
        url='/login',
        status_code=303
    )

#TODO: Protect endpoint
@router.get('/resend_verification')
def resend_verification(
    request: Request,
    db: Session = Depends(get_db),
    user_obj: models.AuthUserModelORM = Depends(oauth2.get_current_user_strict)
):
    verification_token = oauth2.create_token(
        user_data= {"userid": user_obj.userid},
        token_type="verification_token_general"
    ) 
    logging.info(f"Sending email to {user_obj.email} \n with the token: {verification_token}")
    logging.info(f"Confirmation url: {request.url.path} or {request.base_url}auth/verify/{verification_token}")
    return RedirectResponse(
        url='/',
        status_code=303
    )

@router.get('/verify/{verification_token}')
def verify_user(
    request: Request,
    verification_token:str,
    db: Session = Depends(get_db),
    user_obj: models.AuthUserModelORM = Depends(oauth2.get_current_user_strict)
):
    if user_obj.userid == oauth2.verify_token(verification_token, credentials_exception=None, strict=False).userid:
        print(verification_token)
        if not user_obj.verified:
            user_obj.verified = True
            db.add(user_obj)
            db.commit()
        return RedirectResponse(
            url='/index_secure',
            status_code=303
        )
    return RedirectResponse(
        url='/auth/unverified',
        status_code=303
    )

@router.get('/unverified')
def verify_user_info(
    request: Request,
    db: Session = Depends(get_db),
    user_obj: models.AuthUserModelORM = Depends(oauth2.get_current_user_strict)
):
    print('Want to send over a new verification email?')

    return templates.TemplateResponse(
        'auth_unverified.html', {"request": request.headers, "user_obj": user_obj}
    )