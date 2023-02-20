from typing import Union
from pydantic import BaseModel

from datetime import datetime


class UserBase(BaseModel):
    username: str
    firstname: str
    lastname: str
    email: str
    is_pi: bool

    class Config:
        orm_mode = True


# Used as a shortened version of a user object
# to return in json
class UserSignature(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    sponsor_id: Union[int, None]


class PirgBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


# Used as a shortened version of a user object
# to return in json
class PirgSignature(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class PirgCreate(PirgBase):
    owner_id: int
    admin_ids: Union[list[int], None]
    user_ids: Union[list[int], None]


class GroupBase(BaseModel):
    name: str
    pirg_id: int

    class Config:
        orm_mode = True


class GroupCreate(GroupBase):
    pass


class User(UserBase):
    id: int
    sponsor: Union[UserSignature, None]
    pirgs: list[PirgSignature]
    groups: list[GroupBase]
    created_at: datetime
    updated_at: datetime


class Pirg(PirgBase):
    id: int
    owner: UserSignature
    admins: list[UserSignature]
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
