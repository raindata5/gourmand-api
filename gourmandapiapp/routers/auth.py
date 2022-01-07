from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from gourmandapiapp import models, schemas, utils, oauth2
from ..db import get_db
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(tags=['token'])

@router.post('/token')
async def login(login_form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    fetched_user = db.query(models.AuthUserModelORM).filter(models.AuthUserModelORM.email == login_form_data.username).first()
    if not fetched_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect username or password")
    verify_pass = utils.verification(login_form_data.password, fetched_user.password)
    if not verify_pass:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect username or password")
    token = oauth2.create_access_token(user_data= {"userid": fetched_user.userid})
    return {"access_token": token, "token_type": "bearer"}