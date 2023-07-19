from pydantic import BaseModel, ConfigDict
from pydantic.dataclasses import dataclass

from datetime import datetime
from enum import Enum

# TODO(lcrown): nest the return objects in a wrapper like:
# {'status': 'success', 'results': Pirg}
# So then i can make return values more predictable
#

config = ConfigDict(from_attributes=True)


class Status(Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class SimpleStatus(BaseModel):
    status: Status


@dataclass(config=config)
class UserBase:
    username: str
    firstname: str
    lastname: str
    email: str
    is_pi: bool


class UserId(BaseModel):
    user_id: int


# Used as a shortened version of a user object
# to return in json
@dataclass(config=config)
class UserSignature:
    id: int
    username: str


class UserCreate(UserBase):
    sponsor_id: int | None


@dataclass(config=config)
class PirgBase:
    name: str


@dataclass(config=config)
class PirgSignature:
    id: int
    name: str


class PirgCreate(PirgBase):
    owner_id: int
    admin_ids: list[int] | None
    user_ids: list[int] | None


@dataclass(config=config)
class GroupBase:
    name: str


class GroupCreate(GroupBase):
    pirg_id: int
    user_ids: list[int]


@dataclass(config=config)
class GroupSignature:
    id: int
    name: str


# class PirgAddGroup(BaseModel):
#     name: str
#     user_ids: list[int]
#


class PirgGroupName(BaseModel):
    group_name: str


class User(UserBase):
    id: int
    sponsor: UserSignature | None
    pirgs: list[PirgSignature]
    groups: list[GroupBase]
    created_at: datetime
    updated_at: datetime


class Pirg(PirgBase):
    id: int
    owner: UserSignature
    admins: list[UserSignature]
    users: list[UserSignature]
    groups: list[GroupSignature]
    created_at: datetime
    updated_at: datetime


class Group(GroupBase):
    id: int
    pirg: PirgSignature
    users: list[UserSignature]
    created_at: datetime
    updated_at: datetime
