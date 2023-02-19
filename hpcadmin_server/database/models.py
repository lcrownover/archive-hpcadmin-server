from sqlalchemy import String, ForeignKey, Boolean, TIMESTAMP, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .db import Base

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
    sponsor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    sponsor: Mapped["User"] = relationship("User", remote_side=[id])
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
