from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from gourmandapiapp import models, schemas, utils
from ..db import get_db
from typing import Optional
from sqlalchemy.sql.expression import text
from sqlalchemy import desc

router = APIRouter(prefix= '/authusers',
                    tags=['authusers'])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreationResponseSchema)
async def create_user(user_data: schemas.UserLoginSchema,db: Session = Depends(get_db)):
    fetched_user = db.query(models.AuthUserModelORM).filter(models.AuthUserModelORM.email == user_data.email).first()
    if fetched_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="This email is already taken")
    user_data.password = utils.get_password_hash(user_data.password)
    user_obj = models.AuthUserModelORM(**user_data.dict())
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

