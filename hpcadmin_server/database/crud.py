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


class UserAlreadyExistsError(Exception):
    def __init__(self, msg: str = ""):
        if not msg:
            msg = "User already exists"
        super().__init__(msg)


def get_users(db: Session):
    return db.scalars(select(User)).fetchall()


def get_user(db: Session, id: int) -> User:
    return db.scalar(select(User).filter_by(id=id))


def get_user_by_username(db: Session, username: str) -> User:
    return db.scalar(select(User).filter_by(username=username))


def create_user(db: Session, user: schemas.UserCreate) -> User:
    db_user = User(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        sponsor_id=user.sponsor_id,
        is_pi=user.is_pi,
    )
    db.add(db_user)
    try:
        db.commit()
    except:
        db.rollback()
        raise UserAlreadyExistsError(f"User {user.username} already exists")
    db.refresh(db_user)
    return db_user


#####
# Pirgs
#####


class PirgAlreadyExistsError(Exception):
    def __init__(self, msg: str = ""):
        if not msg:
            msg = "Pirg already exists"
        super().__init__(msg)


def get_pirgs(db: Session):
    return db.scalars(select(Pirg)).fetchall()


def get_pirg(db: Session, pirg_id: int) -> Pirg:
    return db.scalar(select(Pirg).filter_by(id=pirg_id))


def get_pirg_by_name(db: Session, name: str) -> Pirg:
    return db.scalar(select(Pirg).filter_by(name=name))


def create_pirg(db: Session, pirg: schemas.PirgCreate) -> Pirg:
    # user objects should have been checked by the pirgs endpoint prior to
    # being enumerated here, so they should always be valid users
    #
    # we skip adding users or admins if they are the owner of the pirg
    users = []
    if pirg.user_ids:
        users = [
            db.scalar(select(User).filter_by(id=user_id))
            for user_id in pirg.user_ids
            if user_id != pirg.owner_id
        ]
    admins = []
    if pirg.admin_ids:
        admins = [
            db.scalar(select(User).filter_by(id=user_id))
            for user_id in pirg.admin_ids
            if user_id != pirg.owner_id
        ]
    db_pirg = Pirg(
        name=pirg.name,
        owner_id=pirg.owner_id,
        admins=admins,
        users=users,
    )
    db.add(db_pirg)
    try:
        db.commit()
    except:
        db.rollback()
        raise PirgAlreadyExistsError(f"Pirg {pirg.name} already exists")
    db.refresh(db_pirg)
    return db_pirg


def add_user_to_pirg(db: Session, pirg: Pirg, user: User) -> Pirg:
    if user.id == pirg.owner_id:
        return pirg
    pirg.users.append(user)
    db.add(pirg)
    db.commit()
    db.refresh(pirg)
    return pirg


def remove_user_from_pirg(db: Session, pirg: Pirg, user: User) -> Pirg:
    pirg.users = [pu for pu in pirg.users if pu.id != user.id]
    db.add(pirg)
    db.commit()
    db.refresh(pirg)
    return pirg


#####
# Groups
#####


class GroupNotFoundError(Exception):
    def __init__(self, msg: str = ""):
        if not msg:
            msg = "Pirg Group not found"
        super().__init__(msg)


class GroupAlreadyExistsError(Exception):
    def __init__(self, msg: str = ""):
        if not msg:
            msg = "Pirg Group already exists"
        super().__init__(msg)


def get_pirg_groups(db: Session):
    return db.scalars(select(Group)).fetchall()


def get_pirg_group(db: Session, group_id: int) -> Group:
    return db.scalar(select(Group).filter_by(id=group_id))


def get_pirg_group_by_name(db: Session, pirg: Pirg, name: str) -> Group:
    return db.scalar(select(Group).filter_by(name=name, pirg_id=pirg.id))


def create_pirg_group(db: Session, group: schemas.GroupCreate) -> Group:
    users = []
    for user_id in group.user_ids:
        db_user = db.scalar(select(User).filter_by(id=user_id))
        if not db_user:
            raise UserNotFoundError(f"User id {user_id} not found")
        users.append(db_user)
    db_group = Group(name=group.name, pirg_id=group.pirg_id, users=users)
    db.add(db_group)
    try:
        db.commit()
    except:
        db.rollback()
        raise GroupAlreadyExistsError(f"Pirg Group {group.name} already exists")
    db.refresh(db_group)
    return db_group


def add_user_to_pirg_group(db: Session, group: Group, user: User) -> Group:
    if user in group.users:
        return group
    group.users.append(user)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def remove_user_from_pirg_group(db: Session, group: Group, user: User) -> Group:
    group.users = [gu for gu in group.users if gu.id != user.id]
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def delete_pirg_group(db: Session, group: Group) -> None:
    db.delete(group)
    db.commit()
    return None
