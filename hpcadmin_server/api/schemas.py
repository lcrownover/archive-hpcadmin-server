from typing import Union
from pydantic import BaseModel

from datetime import datetime


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    firstname: str
    lastname: str
    email: str
    is_pi: bool
    sponsor_id: Union[int, None]


class PirgBase(BaseModel):
    name: str
    owner_id: int


class PirgCreate(PirgBase):
    pass


class PirgAddUser(PirgBase):
    user_id: int


class PirgAddAdmin(PirgBase):
    user_id: int


class PirgAddGroup(PirgBase):
    group_name: str


class GroupBase(BaseModel):
    name: str
    pirg_id: int


class GroupCreate(GroupBase):
    pass


# TODO(lcrown): sponsor not working
class User(UserCreate):
    id: int
    sponsor: Union[UserBase, None]
    pirgs: list[PirgBase]
    groups: list[GroupBase]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Pirg(PirgBase):
    id: int
    owner: UserBase
    admins: list[UserBase]
    users: list[UserBase]
    groups: list[GroupBase]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Group(GroupBase):
    id: int
    pirg: PirgBase
    users: list[UserBase]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
