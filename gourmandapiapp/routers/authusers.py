from sqlalchemy.orm import Session
from gourmandapiapp import models, schemas, utils
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
from fastapi.responses import RedirectResponse
templates = Jinja2Templates(directory="gourmandapiapp/templates")
router = APIRouter(prefix= '/auth',
                    tags=['authusers'])


@router.get('/register')
def get_create_user(request: Request,):
    return templates.TemplateResponse(
        "auth_register.html",
        context={
            "request": request,
        }
    )
@router.post('/register', status_code=status.HTTP_201_CREATED)
async def create_user(
    # user_data: schemas.CreateNewUserSchema,db: Session = Depends(get_db)
    email_input: Annotated[str, Form()],
    password_input: Annotated[str, Form(description='Passwords must match.')],
    password_input_2: Annotated[str, Form(description="The password you signed up with")],
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
    user_obj = models.AuthUserModelORM(
        email=user_data.email_input,
        password=password_input_hash
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return RedirectResponse(
        url='/login',
        status_code=303
    )

