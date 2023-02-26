from sqlalchemy.orm import Session
from sqlalchemy import select

from .models import User, Pirg, Group
from ..api import schemas


#####
# Users
#####


class UserNotFoundError(Exception):
    def __init__(self, msg: str = ""):
        if not msg:
            msg = "User not found"
        super().__init__(msg)


def get_users(db: Session):
    return db.scalar(select(User))


def get_user(db: Session, id: int):
    return db.scalar(select(User).filter_by(id=id))


def get_user_by_username(db: Session, username: str):
    return db.scalar(select(User).filter_by(username=username))


def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        sponsor_id=user.sponsor_id,
        is_pi=user.is_pi,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


#####
# Pirgs
#####


def get_pirgs(db: Session):
    return db.scalars(select(Pirg))


def get_pirg(db: Session, pirg_id: int):
    return db.scalar(select(Pirg).filter_by(id=pirg_id))


def get_pirg_by_name(db: Session, name: str):
    return db.scalar(select(Pirg).filter_by(name=name))


def create_pirg(db: Session, pirg: schemas.PirgCreate):
    # user objects should have been checked by the pirgs endpoint prior to
    # being enumerated here, so they should always be valid users
    users = []
    if pirg.user_ids:
        users = [
            db.scalar(select(User).filter_by(id=user_id)) for user_id in pirg.user_ids
        ]
    admins = []
    if pirg.admin_ids:
        admins = [
            db.scalar(select(User).filter_by(id=user_id)) for user_id in pirg.admin_ids
        ]
    db_pirg = Pirg(
        name=pirg.name,
        owner_id=pirg.owner_id,
        admins=admins,
        users=users,
    )
    db.add(db_pirg)
    db.commit()
    db.refresh(db_pirg)
    return db_pirg


def add_user_to_pirg(db: Session, pirg: Pirg, user: User):
    pirg.users.append(user)
    db.add(pirg)
    db.commit()
    db.refresh(pirg)
    return pirg


def remove_user_from_pirg(db: Session, pirg: Pirg, user: User):
    pirg.users = [pu for pu in pirg.users if pu.id != user.id]
    db.add(pirg)
    db.commit()
    db.refresh(pirg)
    return pirg


#####
# Groups
#####


def get_pirg_groups(db: Session):
    return db.scalars(select(Group))


def get_pirg_group(db: Session, group_id: int):
    return db.scalar(select(Group).filter_by(id=group_id))


def get_pirg_group_by_name(db: Session, name: str):
    return db.scalar(select(Group).filter_by(name=name))


def add_group_to_pirg(db: Session, pirg: Pirg, group: schemas.PirgAddGroup):
    users = []
    for user_id in group.user_ids:
        db_user = db.scalar(select(User).filter_by(id=user_id))
        if not db_user:
            raise UserNotFoundError(f"User id {user_id} not found")
        users.append(db_user)
    db_group = Group(name=group.name, pirg=pirg, users=users)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def add_user_to_pirg_group(db: Session, group: Group, user: User):
    group.users.append(user)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def remove_user_from_pirg_group(db: Session, group: Group, user: User):
    group.users = [gu for gu in group.users if gu.id != user.id]
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def delete_pirg_group(db: Session, group: Group):
    db.delete(group)
    db.commit()
    return None
