from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Boolean, Index
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import DATETIME, Date
from sqlalchemy.dialects.postgresql import (
    TIMESTAMP
)
from sqlalchemy.orm import relationship
from gourmandapiapp.db import Base
from werkzeug.security import generate_password_hash, check_password_hash

class BusinessModelORM(Base):
    __tablename__ = "business"
    businessid = Column(Integer, primary_key=True, nullable=False)
    businessname = Column(String(150), nullable=False)
    chainname = Column(String(150), nullable=False)
    addressline1 = Column(String(150), nullable=True)
    addressline2 = Column(String(150), nullable=True)
    addressline3 = Column(String(150), nullable=True)
    latitude = Column(Numeric(precision=8, scale=6), nullable=True)
    longitude = Column(Numeric(precision=9, scale=6), nullable=True)
    zipcode = Column(String, nullable=True)
    businessphone = Column(String, nullable=True)
    businessurl = Column(String(500), nullable=True)
    is_closed = Column(Boolean, nullable=False)
    distancetocounty = Column(Integer, nullable=True)
    cityid = Column(Integer, nullable=True)
    countyid = Column(Integer, nullable=True)
    stateid = Column(Integer, nullable=True)
    paymentlevelid = Column(Integer, nullable=True)
    lasteditedwhen = Column(TIMESTAMP(precision=6), nullable=False, server_default=text('now()'))
    __table_args__ = (
        Index(
            "ix_business_stateid",
            "stateid",
            
        ),
        Index(
            "ix_business_paymentlevelid",
            "paymentlevelid",
        ),
        Index(
            "ix_business_countyid",
            "countyid",
        ),
        Index(
            "ix_business_cityid",
            "cityid",
        ),
        Index(
            "ix_business_chainname",
            "chainname",
        ),
        {"schema": "_Production"}
    )

class BusinessHoldingModelORM(Base):
    __tablename__ = "businessholding"
    businessholdingid = Column(Integer, primary_key=True, nullable=False)
    businessid = Column(Integer, ForeignKey("_Production.business.businessid", ondelete="CASCADE"), nullable=False)
    businessrating = Column(Numeric(precision=2, scale=1), nullable=True)
    reviewcount = Column(Integer, nullable=True)
    closedate = Column(Date, nullable=False)
    business = relationship("BusinessModelORM")
    __table_args__ = (
        Index(
            "ix_businessholding_businessid",
            "businessid",
        ),
        Index(
            "ix_businessholding_closedate",
            "closedate",
        ),
        {"schema": "_Production"}
    )

class AuthUserModelORM(Base):
    __tablename__ = "authuser"
    __table_args__ = {"schema": "_Production"}
    userid = Column(Integer(), primary_key=True, nullable=False)
    email = Column(String(80), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    created_at = Column(TIMESTAMP(precision=6), nullable = False, server_default=text('now()'))
    verified = Column(Boolean, nullable=False, server_default=text('false'))
    role_id = Column(Integer(), ForeignKey('_Production.role.role_id'))
    role = relationship("Role", back_populates='authuser')


    @property
    def passy(self):
        raise AttributeError("password is not a read attribute")
    
    @passy.setter
    def passy(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class Role(Base):
    __tablename__ = "role"
    __table_args__ = {"schema": "_Production"}
    role_id = Column(Integer, primary_key=True, nullable=False)
    name= Column(String(80), unique=True, nullable=False)
    default = Column(Boolean, nullable=False, server_default=text('false'))
    permissions = Column(Integer(),)
    authuser = relationship("AuthUserModelORM", back_populates='role', lazy="dynamic")
    
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0
    
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm
    def reset_permissions(self):
        self.permissions = 0
    def has_permission(self, perm):
        return self.permissions & perm == perm

    __table_args__ = (
        Index(
            "ix_role_default",
            "default",
        ),
        {"schema": "_Production"}
    )

if __name__ == "__main__":
    user = AuthUserModelORM()
    role = Role(name='COMMENT')
    print(role.name)
    print(role.permissions)