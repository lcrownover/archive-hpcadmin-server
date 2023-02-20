from typing import Optional
from sqlalchemy import String, ForeignKey, Boolean, TIMESTAMP, Column, Table, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .db import Base

pirg_user_association_table = Table(
    "pirg_user_association_table",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("pirg_id", Integer, ForeignKey("pirgs.id")),
)

pirg_admin_association_table = Table(
    "pirg_admin_association_table",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("pirg_id", Integer, ForeignKey("pirgs.id")),
)

pirg_group_association_table = Table(
    "pirg_group_association_table",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("pirg_id", Integer, ForeignKey("pirgs.id")),
    Column("group_id", Integer, ForeignKey("groups.id")),
)

group_user_association_table = Table(
    "group_user_association_table",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
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
    sponsor_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
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
