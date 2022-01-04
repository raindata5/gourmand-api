from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import DATETIME, TIMESTAMP
from sqlalchemy.orm import relationship
from .db import Base

class BusinessModelORM(Base):
    __tablename__ = "business"
    businessid = Column(Integer, primary_key=True, nullable=False)
    businessname = Column(String, nullable=False)
    chainname = Column(String, nullable=False)
    addressline1 = Column(String, nullable=False)
    addressline2 = Column(String, nullable=True)
    addressline3 = Column(String, nullable=True)
    latitude = Column(Numeric, precision=8, scale=6)
    longitude = Column(Numeric, precision=9, scale=6)
    zipcode = Column(String, nullable=True)
    businessphone = Column(String, nullable=True)
    businessurl = Column(String(500), nullable=True)
    is_closed = Column
    #alter is_closed to boolean
    # businessname text COLLATE pg_catalog."default",
    # chainname text COLLATE pg_catalog."default",
    # addressline1 text COLLATE pg_catalog."default",
    # addressline2 character varying(100) COLLATE pg_catalog."default",
    # addressline3 character varying(100) COLLATE pg_catalog."default",
    # latitude numeric,
    # longitude numeric,
    # zipcode character varying(50) COLLATE pg_catalog."default",
    # businessphone character varying(50) COLLATE pg_catalog."default",
    # businessurl character varying(500) COLLATE pg_catalog."default",
    # is_closed integer,
    # distancetocounty integer,
    # cityid integer,
    # countyid integer,
    # stateid integer,
    # paymentlevelid integer,
    # lasteditedwhen timestamp(3) without time zone,