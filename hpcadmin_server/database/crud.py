from sqlalchemy.orm import Session

from . import models
from ..api import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
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
    return db.query(models.Pirg).filter(models.Pirg.id == pirg_id).first()


def get_pirg_by_name(db: Session, name: str):
    return db.query(models.Pirg).filter(models.Pirg.name == name).first()


def get_pirgs(db: Session):
    return db.query(models.Pirg).all()


def create_pirg(db: Session, pirg: schemas.PirgCreate):
    owner = db.query(models.User).filter(models.User.id == pirg.owner_id).first()
    if not owner:
        raise Exception("error findiner user in database")
    db_pirg = models.Pirg(
        name=pirg.name,
        owner_id=owner.id,
    )
    db.add(db_pirg)
    db.commit()
    db.refresh(db_pirg)
    return db_pirg


def add_user_to_pirg(db: Session, pirg: models.Pirg, user: models.User):
    pirg.users.append(user)
    db.add(pirg)
    db.commit()
    db.refresh(pirg)
    return pirg


###
# Groups
###


def get_groups(db: Session):
    return db.query(models.Group).all()
