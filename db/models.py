from __future__ import annotations
from typing import ClassVar, List
from db.database import Base
from sqlalchemy import Boolean, Column, Date, ForeignKey, String, Time
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True)
    box_id: Mapped[int] = Column(Integer, ForeignKey("boxes.id"))
    first_name: Mapped[str] = Column(String)
    last_name: Mapped[str] = Column(String)
    email: Mapped[str] = Column(String, unique=True, index=True)
    password_hash: Mapped[str] = Column(String)
    is_staff: Mapped[bool] = Column(Boolean, default=False)
    attendances = relationship("Attendance", back_populates="owner")

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True)
    attendees_count = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="attendances")


class Box(Base):
    __tablename__ = "boxes"

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String)


class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String)
    type: Mapped[str] = Column(String)
    date: Mapped[str] = Column(Date)
    time: Mapped[str] = Column(Time)

class News(Base):
    __tablename__ = "news"


    id: Mapped[int] = Column(Integer, primary_key=True)
    title: Mapped[str] = Column(String)
    body: Mapped[str] = Column(String)
    date: Mapped[str] = Column(Date)

class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String)
    description: Mapped[str] = Column(String)
    date: Mapped[str] = Column(Date)