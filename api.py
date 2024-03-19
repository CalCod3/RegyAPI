from datetime import date
from typing import Annotated
from uuid import UUID
from db.schemas import Athlete, Attendance, Box, Event, News, Workout
from fastapi import FastAPI, Depends, HTTPException
import auth
import admin.admin as admin
import db.models as models
from db.database import Base, SessionLocal, engine, get_db
from sqlalchemy.orm import Session

app = FastAPI()
app.include_router(auth.router)
app.include_router(admin.router)

models.Base.metadata.create_all(bind = engine)

db_dependency = Annotated[Session,  Depends(get_db)]

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

@app.get("/api/classes")
async def get_classes(db: db_dependency):
    return db.query(models.ClassRoom).all()
    
@app.get("/api/attendance/{user_id}")
async def get_attendance(user_id: int, db: db_dependency):
    query = db.query(models.User).filter(models.User.id == user_id)
    return query


@app.get("/api/workouts/{workout_id}")
async def get_workout_by_id(workout_id: int, db: db_dependency):

    workout_model = db.query(models.Workout).filter(models.Workout.id == workout_id).first()

    if workout_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"Workout with ID {workout_id} Does not exist"
        )
    
    return workout_model

@app.get("/api/workouts/{workout_type}")
async def get_workout_by_type(workout_type: str, db: db_dependency):

    workout_model = db.query(models.Workout).filter(models.Workout.type == workout_type).first()

    if workout_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"Workout of type {workout_type} Does not exist"
        )
    
    return workout_model

@app.get("/api/news/{news_id}")
async def get_news_by_id(news_id: int, db: db_dependency):

    news_model = db.query(models.News).filter(models.News.id == news_id).first()

    if news_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"News of ID {news_id} Does not exist"
        )
    
    return news_model

@app.get("/api/events/{event_id}")
async def get_event_by_id(event_id: int, db: db_dependency):

    event_model = db.query(models.Event).filter(models.Event.id == event_id).first()

    if event_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"Event of ID {event_id} Does not exist"
        )
    
    return event_model