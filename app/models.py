from sqlite3 import SQLITE_LIMIT_VARIABLE_NUMBER
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, func, Enum as SQLEnum
from app.database import Base
from enum import Enum


#  House Model


class House(Base):
    __tablename__ = "house_informations"

    id = Column(Integer, primary_key=True, index=True)
    SellerID = Column(Integer)
    AddressNumber = Column(Integer)
    StreetName = Column(String)
    DayTime = Column(DateTime, default=func.now())
    Respond = Column(Boolean)
    Size = Column(String)
    SecurityGameOrAlarm = Column(Boolean)
    Dog = Column(String)
    Age = Column(String)
    Gender = Column(String)
    Price = Column(Float)


#  User Model

"""
class UserStatus(Enum):
    ADMIN = "admin"
    UNAUTHORIZED = "unauthorized"
    AUTHORIZED = "authorized"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    FirstName = Column(String)
    LastName = Column(String)
    Email = Column(String)
    Password = Column(String)
    #  Status = Column(SQLEnum(UserStatus), nullable=False, default=UserStatus.UNAUTHORIZED)
    Access = Column(Boolean, default=False)
"""

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    full_name = Column(String)
    disabled = Column(Boolean)
    hashed_password = Column(String)
