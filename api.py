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
    is_staff: bool = False

    class Config:
        orm_mode = True

class Box(BaseModel):
    name: str

    class Config:
        orm_mode = True


@app.get("/api/athletes")
async def get_athletes(db: db_dependency):
    return db.query(models.User).filter(models.User.is_staff == False)


@app.put("/api/athletes/{athlete_id}")
async def update_athlete(athlete: Athlete, athlete_id: int, db: db_dependency):
    athlete_model = db.query(models.User).filter(models.User.id == athlete_id).first()

    if athlete_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"Athlete with ID {athlete_id} Does not exist"
        )
    
    athlete_model.username = athlete.username  # type: ignore
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
    
    box_model.name = athlete.name  # type: ignore
    box_model.email = athlete.email  # type: ignore

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
