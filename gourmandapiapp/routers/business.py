from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from gourmandapiapp import models, oauth2
from ..db import get_db
from typing import Optional
from sqlalchemy.sql.expression import text
from sqlalchemy import desc


router = APIRouter(prefix= '/businesses',
                    tags=['business'])



@router.get('/{business_id}')
async def get_business(business_id: int, db: Session = Depends(get_db)):
    return db.query(models.BusinessModelORM).filter(models.BusinessModelORM.businessid == business_id).first()

# perhaps revise the sort so either asc or desc can be chosen
# also look to refactor refering to column object directly (take input, iterate through tables columns and pick one)
@router.get('/')
async def get_businesses(limit: Optional[int] = 100, offset: Optional[int] = None,  keyword: Optional[str] = '', sort: Optional[str] = 'businessname',db: Session = Depends(get_db)):
    return db.query(models.BusinessModelORM).filter(models.BusinessModelORM.chainname.contains(keyword)).order_by(desc(sort)).limit(limit).offset(offset).all()

@router.post('/')
async def post_business( db: Session = Depends(get_db), user_obj: models.AuthUserModelORM = Depends(oauth2.get_current_user)):
    return {"result": "business updated"}