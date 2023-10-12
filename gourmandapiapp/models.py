from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import DATETIME, TIMESTAMP, Date
from sqlalchemy.orm import relationship
from gourmandapiapp.db import Base
from werkzeug.security import generate_password_hash, check_password_hash

class BusinessModelORM(Base):
    __tablename__ = "business"
    __table_args__ = {"schema": "_Production"}
    businessid = Column(Integer, primary_key=True, nullable=False)
    businessname = Column(String, nullable=False)
    chainname = Column(String, nullable=False)
    addressline1 = Column(String, nullable=False)
    addressline2 = Column(String, nullable=True)
    addressline3 = Column(String, nullable=True)
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
    lasteditedwhen = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    

class BusinessHoldingModelORM(Base):
    __tablename__ = "businessholding"
    __table_args__ = {"schema": "_Production"}
    businessholdingid = Column(Integer, primary_key=True, nullable=False)
    # businessid = Column(Integer, ForeignKey("_Production.business.businessid", ondelete="CASCADE"), nullable=False)
    businessid = Column(Integer, ForeignKey("business.businessid", ondelete="CASCADE"), nullable=False)
    businessrating = Column(Numeric(precision=2, scale=1), nullable=True)
    reviewcount = Column(Integer, nullable=True)
    closedate = Column(Date, nullable=False)
    business = relationship("BusinessModelORM")

class AuthUserModelORM(Base):
    __tablename__ = "authuser"
    __table_args__ = {"schema": "_Production"}
    userid = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(60), unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))
    # verified = Column(Boolean, nullable=False, default=False)

    @property
    def passy(self):
        raise AttributeError("password is not a read attribute")
    
    @passy.setter
    def passy(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

if __name__ == "__main__":
    user = AuthUserModelORM()