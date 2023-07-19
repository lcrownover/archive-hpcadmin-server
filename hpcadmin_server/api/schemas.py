from pydantic import BaseModel

from datetime import datetime
from enum import Enum

# TODO(lcrown): nest the return objects in a wrapper like:
# {'status': 'success', 'results': Pirg}
# So then i can make return values more predictable
#


class Status(Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class SimpleStatus(BaseModel):
    status: Status


class UserBase(BaseModel):
    username: str
    firstname: str
    lastname: str
    email: str
    is_pi: bool

    class ConfigDict:
        from_attributes = True


class UserId(BaseModel):
    user_id: int


# Used as a shortened version of a user object
# to return in json
class UserSignature(BaseModel):
    id: int
    username: str

    class ConfigDict:
        from_attributes = True


class UserCreate(UserBase):
    sponsor_id: int | None


class PirgBase(BaseModel):
    name: str

    class ConfigDict:
        from_attributes = True


class PirgSignature(BaseModel):
    id: int
    name: str

    class ConfigDict:
        from_attributes = True


class PirgCreate(PirgBase):
    owner_id: int
    admin_ids: list[int] | None
    user_ids: list[int] | None


class GroupBase(BaseModel):
    name: str

    class ConfigDict:
        from_attributes = True


class GroupCreate(GroupBase):
    pirg_id: int
    user_ids: list[int]


class GroupSignature(BaseModel):
    id: int
    name: str

    class ConfigDict:
        from_attributes = True


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
