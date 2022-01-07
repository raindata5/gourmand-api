from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from gourmandapiapp import models, oauth2, schemas
from ..db import get_db, start_redis
from typing import Optional, Any
from sqlalchemy.sql.expression import text
from sqlalchemy import desc
import json
from datetime import time, timedelta


router = APIRouter(prefix= '/businesses',
                    tags=['business'])



@router.get('/{business_id}', response_model=schemas.BusinessResponseSchema)
async def get_business(business_id: int, db: Session = Depends(get_db),  redis_client: Any = Depends(start_redis)):
    try:
        print(redis_client)
        cached_language_data = None
        cached_language_data = redis_client.get(f"business:{business_id}")
    except Exception as e:
        print(e)

    if cached_language_data:
        try:
            cached_language_data = json.loads(cached_language_data)
            cached_language_data

            print('Used Redis')
            return cached_language_data
        except Exception as e:
            print(e)
        
    business = db.query(models.BusinessModelORM).filter(models.BusinessModelORM.businessid == business_id).first()
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No business exists under this id")
    business_model = schemas.dict_request(business, inc_json_dump=True)
    redis_client.set(f"business:{business_id}", business_model)
    redis_client.expire(f"business:{business_id}", timedelta(minutes=5))
    print('Used Postgres')
    return business

# perhaps revise the sort so either asc or desc can be chosen
# also look to refactor refering to column object directly (take input, iterate through tables columns and pick one)
@router.get('/')
async def get_businesses(limit: Optional[int] = 100, offset: Optional[int] = None,  keyword: Optional[str] = '', sort: Optional[str] = 'businessname',db: Session = Depends(get_db)):
    businesses = db.query(models.BusinessModelORM).filter(models.BusinessModelORM.chainname.contains(keyword)).order_by(desc(sort)).limit(limit).offset(offset).all()

    return businesses

@router.post('/')
async def post_business( db: Session = Depends(get_db), user_obj: models.AuthUserModelORM = Depends(oauth2.get_current_user)):
    return {"result": "business inserted"}

@router.put('/')
async def update_business( db: Session = Depends(get_db), user_obj: models.AuthUserModelORM = Depends(oauth2.get_current_user)):
    return {"result": f"business updated by {user_obj.userid}"}