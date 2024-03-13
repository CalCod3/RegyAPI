from pydantic import BaseModel, EmailStr, Field
from datetime import date


class Athlete(BaseModel):
    first_name: str
    last_name: str
    box_id: int
    email: EmailStr
    is_staff: bool = False

    class Config:
        orm_mode = True

class Box(BaseModel):
    name: str

    class Config:
        orm_mode = True

class Attendance(BaseModel):
    date: date
    owner_id: int

class Workout(BaseModel):
    name: str
    type: str
    date: str
    time: str

class News(BaseModel):
    title: str
    body: str
    date: str

class Event(BaseModel):
    name: str
    description: str
    date: str