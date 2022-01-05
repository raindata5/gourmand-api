from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from gourmandapiapp import models
from ..db import get_db
from typing import Optional
from sqlalchemy.sql.expression import text
from sqlalchemy import desc, asc


router = APIRouter(prefix= '/businessholdings',
                    tags=['businessholdings'])



@router.get('/{business_id}')
async def get_businessholdings_business(business_id: int, db: Session = Depends(get_db)):
    return db.query(models.BusinessHoldingModelORM).filter(models.BusinessHoldingModelORM.businessid == business_id).all()

# perhaps revise the sort so either asc or desc can be chosen
# also look to refactor refering to column object directly (take input, iterate through tables columns and pick one)
@router.get('/')
async def get_businessholdings(limit: Optional[int] = 100, offset: Optional[int] = None, sort: Optional[str] = 'closedate',db: Session = Depends(get_db)):
    query = db.query(models.BusinessHoldingModelORM).order_by(desc(sort)).limit(limit).offset(offset)
    print(query)
    return query.all()
    