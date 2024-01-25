from __future__ import annotations
from typing import ClassVar, List
from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True)
    box_id: Mapped[int] = Column(Integer, ForeignKey("boxes.id"))
    box: Mapped[str] = relationship("Box", back_populates="members")
    first_name: Mapped[str] = Column(String)
    last_name: Mapped[str] = Column(String)
    email: Mapped[str] = Column(String, unique=True, index=True)
    password_hash: Mapped[str] = Column(String)
    is_staff: Mapped[bool] = Column(Boolean, default=False)


class Box(Base):
    __tablename__ = "boxes"

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String)
    members: Mapped[List["User"]] = relationship("User", back_populates="box")


