from datetime import datetime
import json
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from email_validator import validate_email

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserCreationResponseSchema(BaseModel):
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True 

class BusinessResponseSchema(BaseModel):
    businessid: int
    businessname: str
    chainname: str
    addressline1: str
    addressline2: str
    addressline3: str
    latitude: float
    longitude: float
    zipcode: str
    businessphone: str
    businessurl: str
    is_closed: bool
    distancetocounty: int
    cityid: int
    countyid: int
    stateid: int
    paymentlevelid: int
    lasteditedwhen: datetime
    class Config:
        orm_mode = True 

class TokenData(BaseModel):
    userid: int

# converts model object into a python dictionary or into a json string through parameter
def dict_request(orm_model, inc_json_dump=False):
    d = {}
    for column in orm_model.__table__.columns:
        d[column.name] = str(getattr(orm_model, column.name))
    if not inc_json_dump:
        return d
    else:
        return json.dumps(d)