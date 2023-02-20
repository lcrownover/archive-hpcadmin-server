from typing import Union
from pydantic import BaseModel

from datetime import datetime


class UserBase(BaseModel):
    pass

    class Config:
        orm_mode = True


class UserSignature(UserBase):
    id: int
    username: str


class UserCreate(UserBase):
    username: str
    firstname: str
    lastname: str
    email: str
    is_pi: bool
    sponsor_id: Union[int, None]


class PirgBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class PirgCreate(PirgBase):
    owner_id: int


class GroupBase(BaseModel):
    name: str
    pirg_id: int

    class Config:
        orm_mode = True


class GroupCreate(GroupBase):
    pass


class User(UserCreate):
    id: int
    pirgs: list[PirgBase]
    groups: list[GroupBase]
    created_at: datetime
    updated_at: datetime


class Pirg(PirgBase):
    id: int
    owner: UserSignature
    admins: list[UserBase]
    users: list[UserSignature]
    groups: list[GroupBase]
    created_at: datetime
    updated_at: datetime


class Group(GroupBase):
    id: int
    pirg: PirgBase
    users: list[UserBase]
    created_at: datetime
    updated_at: datetime


#####
# These are used in transactions and don't represent models in the database
#####


class PirgAddUser(BaseModel):
    user_id: int


class PirgAddAdmin(BaseModel):
    user_id: int


class PirgAddGroup(BaseModel):
    group_name: str
