from datetime import datetime
import json
from pydantic import BaseModel, EmailStr, Field
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
    addressline2: Optional[str] = None
    addressline3: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    zipcode: Optional[str] = None
    businessphone: Optional[str] = None
    businessurl: Optional[str] = None
    is_closed: bool
    distancetocounty: Optional[int] = None
    cityid: Optional[int] = None
    countyid: Optional[int] = None
    stateid: Optional[int] = None
    paymentlevelid: Optional[int] = None
    lasteditedwhen: datetime
    class Config:
        orm_mode = True 

class TokenData(BaseModel):
    userid: int


class PullDataSchema(BaseModel):
    limit: Optional[int] = Field(0, title=" the desired amount of results must be between 0 and 100", ge = 0, le=100 )
    offset: Optional[int] = Field(0, title=" the desired amount of results passed over must be between 0 and 50", ge = 0, le=50 )
    keyword: Optional[str] = Field('', max_length=100 )
    sort: Optional[str] = Field('businessname', max_length=100 )

# converts model object into a python dictionary or into a json string through parameter
def dict_request(orm_model, inc_json_dump=False):
    d = {}
    for column in orm_model.__table__.columns:
        d[column.name] = str(getattr(orm_model, column.name))
    if not inc_json_dump:
        return d
    else:
        return json.dumps(d)