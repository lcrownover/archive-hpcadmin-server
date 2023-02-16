# TODO(lcrown): determine if i want users to be nested inside pirgs
# or if i'd rather just have a list of ids and expect the user to get the objects for each id
# if the former, how would I add an admin to a pirg?

from fastapi import FastAPI

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


class UserOrm(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(255))
    lastname: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(255), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    pirgs: Mapped[list["PirgOrm"]] = relationship(
        secondary=pirg_user_association_table, back_populates="users"
    )
    sponsor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    is_pi: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class PirgOrm(Base):
    __tablename__ = "pirgs"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    owner: Mapped["UserOrm"] = mapped_column(ForeignKey("users.id"))
    admins: Mapped[list["UserOrm"]] = relationship(
        secondary=pirg_admin_association_table
    )
    users: Mapped[list["UserOrm"]] = relationship(
        secondary=pirg_user_association_table, back_populates="pirgs"
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


class UserModel(UserBaseModel):
    pirgs: list[PirgBaseModel]


class PirgModel(PirgBaseModel):
    owner: UserBaseModel
    users: list[UserBaseModel]


engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/users")
async def get_users():
    with Session(engine) as session:
        statement = select(UserOrm)
        users = []
        for user in session.scalars(statement):
            users.append(UserModel.from_orm(user))
        return users


@app.post("/users")
async def post_users():
    with Session(engine) as session:
        new_user = UserOrm(
            firstname="lucas",
            lastname="crownover",
            username="lcrown",
            email="lcrown@uoregon.edu",
            is_pi=True,
        )
        session.add(new_user)
        session.commit()


@app.get("/pirgs")
async def get_pirgs():
    with Session(engine) as session:
        statement = select(PirgOrm)
        pirgs = []
        for pirg in session.scalars(statement):
            pirgs.append(PirgModel.from_orm(pirg))
        return pirgs


@app.post("/pirgs")
async def post_pirgs():
    with Session(engine) as session:
        stmt = select(UserOrm).where(UserOrm.username == "lcrown")
        user = session.scalar(stmt)
        new_pirg = PirgOrm(
            name="pirgOne",
            owner=user.id,
            users=[user],
        )
        session.add(new_pirg)
        session.commit()
