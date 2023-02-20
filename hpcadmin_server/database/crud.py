from sqlalchemy.orm import Session
from sqlalchemy import select

from .models import User, Pirg, Group
from ..api import schemas


#####
# Users
#####


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


#####
# Groups
#####


def get_groups(db: Session):
    return db.scalars(select(Group))
