from typing import Annotated
from uuid import UUID
from fastapi import FastAPI, Depends, HTTPException
import auth
from pydantic import BaseModel, EmailStr, Field
import models
from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()
app.include_router(auth.router)

models.Base.metadata.create_all(bind = engine)

def get_db():

    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

        
db_dependency = Annotated[Session,  Depends(get_db)]

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

class ClassRoom(BaseModel):
    date: str


@app.get("/api/athletes")
async def get_athletes(db: db_dependency):
    query = db.query(models.User).all()
    print(query)
    return query

@app.get("/api/athletes/{athlete_id}")
async def get_athlete_by_id(athlete_id: int, db: db_dependency):
    athlete_model = db.query(models.User).filter(models.User.id == athlete_id).first()

    if athlete_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"Athlete with ID {athlete_id} Does not exist"
        )
    
    return athlete_model

@app.put("/api/athletes/{athlete_id}")
async def update_athlete(athlete: Athlete, athlete_id: int, db: db_dependency):
    athlete_model = db.query(models.User).filter(models.User.id == athlete_id).first()

    if athlete_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"Athlete with ID {athlete_id} Does not exist"
        )
    
    athlete_model.first_name = athlete.first_name  # type: ignore
    athlete_model.last_name = athlete.last_name
    athlete_model.email = athlete.email  # type: ignore

    db.add(athlete_model)
    db.commit()
    return athlete

@app.delete("/api/athletes/{athlete_id}")
async def delete_athlete(athlete_id: int, db: db_dependency):

    athlete_model = db.query(models.User).filter(models.User.id == athlete_id).first()

    if athlete_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"Athlete with ID {athlete_id} Does not exist"
        )
    
    db.query(models.User).filter(models.User.id == athlete_id).delete()

    db.commit()

@app.get("/api/boxes")
async def get_boxes(db: db_dependency):
    return db.query(models.Box).all()
    

@app.post("/api/boxes/new")
async def create_box(box: Box, db: db_dependency):
    box_model = models.Box()

    box_model.name = box.name  # type: ignore

    db.add(box_model)
    db.commit()
    return box


@app.put("/api/boxes/{box_id}")
async def update_box(box: Box, box_id: int, db: db_dependency):
    box_model = db.query(models.Box).filter(models.Box.id == box_id).first()

    if box_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"Box with ID {box_id} Does not exist"
        )
    
    box_model.name = box.name  # type: ignore

    db.add(box_model)
    db.commit()
    return box

@app.delete("/api/boxes/{box_id}")
async def delete_box(box_id: int, db: db_dependency):

    box_model = db.query(models.Box).filter(models.Box.id == box_id).first()

    if box_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"Box with ID {box_id} Does not exist"
        )
    
    db.query(models.Box).filter(models.Box.id == box_id).delete()

    db.commit()

@app.get("/api/classes")
async def get_classes(db: db_dependency):
    return db.query(models.ClassRoom).all()
    
@app.get("/api/attendance/{user_id}")
async def get_attendance(user_id: int, db: db_dependency):
    query = db.query(models.User).filter(models.User.id == user_id)
    return query.attendances
    

@app.post("/api/attendance/new")
async def create_attendance(classroom: ClassRoom, db: db_dependency):
    class_model = models.Attendance()

    class_model.date = classroom.date  # type: ignore

    db.add(class_model)
    db.commit()
    return classroom


@app.delete("/api/attendance/{user_id}")
async def delete_attendance(user_id: int, db: db_dependency):

    class_model = db.query(models.Attendance).filter(models.Attendance.user_id == user_id).first()

    if class_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"Attendance for user with ID {user_id} Does not exist"
        )
    
    db.query(models.Attendance).filter(models.Attendance.user_id == user_id).delete()

    db.commit()

