from sqlalchemy.orm import Session
from sqlalchemy import select

from .models import User, Pirg, Group
from ..api import schemas


def get_user(db: Session, user_id: int):
    return db.query(User).filter_by(id=user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter_by(username=username).first()


def get_users(db: Session):
    return db.query(User).all()


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


def get_pirg(db: Session, pirg_id: int):
    # return (
    #     db.query(Pirg)
    #     .join(Pirg.users)
    #     .filter(Pirg.id == pirg_id)
    #     .first()
    # )
    statement = select(Pirg).filter_by(id=pirg_id)
    return db.scalar(statement)


def get_pirg_by_name(db: Session, pirg_name: str):
    statement = select(Pirg).filter_by(name=pirg_name)
    return db.scalar(statement)
    # return (
    #     db.query(Pirg)
    #     .join(Pirg.users)
    #     .filter(Pirg.name == pirg_name)
    #     .first()
    # )


def get_pirgs(db: Session):
    return db.query(Pirg).all()


def create_pirg(db: Session, pirg: schemas.PirgCreate):
    # Check to make sure the owner exists,
    # otherwise raise an error
    owner = db.query(User).filter(User.id == pirg.owner_id).first()
    if not owner:
        raise Exception("error findiner user in database")
    # Create the pirg with the minimum requirements
    db_pirg = Pirg(
        name=pirg.name,
        owner_id=pirg.owner_id,
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


###
# Groups
###


def get_groups(db: Session):
    return db.query(Group).all()
