from pydantic import BaseModel
from typing import Optional
import datetime


#  Houses Templates


class House(BaseModel):
    id: int
    SellerID: int
    AddressNumber: int
    StreetName: str
    DayTime: datetime.datetime
    Respond: bool
    Size: str
    SecurityGameOrAlarm: bool
    Dog: str
    Age: str
    Gender: str
    Price: float


class HouseCreate(BaseModel):
    SellerID: int
    AddressNumber: int
    StreetName: str
    Respond: bool
    Size: str
    SecurityGameOrAlarm: bool
    Dog: str
    Age: str
    Gender: str
    Price: float

    class Config:
        from_attributes = True
        extra = "forbid"


class HouseUpdate(BaseModel):
    AddressNumber: Optional[int] = None
    StreetName: Optional[str] = None
    Respond: Optional[bool] = None
    Size: Optional[str] = None
    SecurityGameOrAlarm: Optional[bool] = None
    Dog: Optional[str] = None
    Age: Optional[str] = None
    Gender: Optional[str] = None
    Price: Optional[float] = None

    class Config:
        from_attributes = True
        extra = "forbid"


class HouseResponse(House):

    class Config:
        from_attributes = True


#  User Templates

"""
class User(BaseModel):
    id: int
    FirstName: str
    LastName: str
    Email: str
    Password: str
    Access: bool
    SuperUser: bool


class UserFormCreate(BaseModel):
    FirstName: set
    LastName: str
    Email: str
    Password: str
"""

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str

