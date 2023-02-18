# TODO(lcrown): determine if i want users to be nested inside pirgs
# or if i'd rather just have a list of ids and expect the user to get the objects for each id
# if the former, how would I add an admin to a pirg?

from fastapi import FastAPI, HTTPException

from sqlalchemy import String, ForeignKey, Boolean, TIMESTAMP, Column, Table
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from typing import Optional
from pydantic import BaseModel

from datetime import datetime

Base = declarative_base()

pirg_user_association_table = Table(
    "pirg_user_association_table",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("pirg_id", ForeignKey("pirgs.id"), primary_key=True),
)

pirg_admin_association_table = Table(
    "pirg_admin_association_table",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("pirg_id", ForeignKey("pirgs.id"), primary_key=True),
)

pirg_group_association_table = Table(
    "pirg_group_association_table",
    Base.metadata,
    Column("pirg_id", ForeignKey("pirgs.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)

group_user_association_table = Table(
    "group_user_association_table",
    Base.metadata,
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    firstname: Mapped[str] = mapped_column(String(255))
    lastname: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    pirgs: Mapped[list["Pirg"]] = relationship(
        secondary=pirg_user_association_table, back_populates="users"
    )
    groups: Mapped[list["Group"]] = relationship(
        secondary=group_user_association_table, back_populates="users"
    )
    sponsor: Mapped[int] = mapped_column(ForeignKey("users.username"), nullable=True)
    is_pi: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Pirg(Base):
    __tablename__ = "pirgs"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship()
    admins: Mapped[list["User"]] = relationship(secondary=pirg_admin_association_table)
    users: Mapped[list["User"]] = relationship(
        secondary=pirg_user_association_table, back_populates="pirgs"
    )
    groups: Mapped[list["Group"]] = relationship(secondary=pirg_group_association_table)
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    pirg: Mapped["Pirg"] = relationship(
        secondary=pirg_group_association_table, back_populates="groups"
    )
    users: Mapped[list["User"]] = relationship(
        secondary=group_user_association_table, back_populates="groups"
    )
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class UserBaseModel(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    sponsor_id: Optional[int]
    is_pi: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PirgBaseModel(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class GroupBaseModel(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserModel(UserBaseModel):
    pirgs: list[PirgBaseModel]
    groups: list[GroupBaseModel]


class PirgModel(PirgBaseModel):
    owner: UserBaseModel
    admins: list[UserBaseModel]
    users: list[UserBaseModel]
    groups: list[GroupBaseModel]


class GroupModel(GroupBaseModel):
    pirg: PirgBaseModel
    users: list[UserBaseModel]


engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/users")
async def get_users():
    with Session(engine) as session:
        statement = select(User)
        users = []
        for user in session.scalars(statement):
            users.append(UserModel.from_orm(user))
        return users


@app.post("/users")
async def post_users():
    with Session(engine) as session:
        new_user1 = User(
            firstname="Lucas",
            lastname="Crownover",
            username="lcrown",
            email="lcrown@uoregon.edu",
            is_pi=True,
        )
        session.add(new_user1)
        session.commit()

        new_user2 = User(
            firstname="Mark",
            lastname="Allen",
            username="marka",
            email="marka@uoregon.edu",
            is_pi=True,
        )
        session.add(new_user2)
        session.commit()


@app.get("/pirgs")
async def get_pirgs():
    with Session(engine) as session:
        statement = select(Pirg)
        pirgs = []
        for pirg in session.scalars(statement):
            pirgs.append(PirgModel.from_orm(pirg))
        return pirgs


@app.post("/pirgs")
async def post_pirgs():
    with Session(engine) as session:
        pirg_name = "pirgOne"
        # Get the owner from the db
        owner_username = "lcrown"
        stmt = select(User).where(User.username == owner_username)
        owner = session.scalar(stmt)
        if not owner:
            raise HTTPException(
                status_code=404, detail=f"user not found: {owner_username}"
            )

        user_username = "marka"
        stmt = select(User).where(User.username == user_username)
        user = session.scalar(stmt)
        if not user:
            raise HTTPException(
                status_code=404, detail=f"user not found: {user_username}"
            )

        new_pirg = Pirg(
            name=pirg_name,
            owner=owner,
            admins=[user],
            users=[user],
        )

        session.add(new_pirg)
        session.commit()

        stmt = select(Pirg).where(Pirg.name == pirg_name)
        pirg = session.scalar(stmt)
        if not pirg:
            raise HTTPException(status_code=404, detail=f"pirg not found: {pirg_name}")
        group1 = Group(name="bestgroup", pirg=pirg, users=[owner, user])
        group2 = Group(name="notasgoodgroup", pirg=pirg, users=[owner, user])
        pirg.groups = [group1, group2]
        session.add(pirg)
        session.commit()


@app.get("/groups")
async def get_groups():
    with Session(engine) as session:
        statement = select(Group)
        groups = []
        for group in session.scalars(statement):
            groups.append(GroupModel.from_orm(group))
        return groups
