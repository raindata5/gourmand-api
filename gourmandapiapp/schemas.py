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


class TokenData(BaseModel):
    userid: int