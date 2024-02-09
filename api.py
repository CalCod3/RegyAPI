from typing import Annotated
from uuid import UUID
from fastapi import FastAPI, Depends, HTTPException
import auth
from pydantic import BaseModel, EmailStr, Field
import db.models as models
from db.database import Base, SessionLocal, engine
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

@app.post("/api/workouts/new")
async def create_workout(workout: Workout, db: db_dependency):
    workout_model = models.Workout()

    workout_model.name = workout.name
    workout_model.type = workout.type
    workout_model.date = workout.date
    workout_model.time = workout.time 

    db.add(workout_model)
    db.commit()
    return workout

@app.put("/api/workouts/{workout_id}")
async def update_workout(workout: Workout, workout_id: int, db: db_dependency):
    workout_model = db.query(models.Workout).filter(models.Workout.id == workout_id).first()

    if workout_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"Workout with ID {workout_id} Does not exist"
        )
    
    workout_model.name = workout.name
    workout_model.type = workout.type
    workout_model.date = workout.date
    workout_model.time = workout.time 

    db.add(workout_model)
    db.commit()
    return workout

@app.delete("/api/workouts/{workout_id}")
async def delete_workout(workout_id: int, db: db_dependency):

    workout_model = db.query(models.Workout).filter(models.Workout.id == workout_id).first()

    if workout_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"Workout with ID {workout_id} Does not exist"
        )
    
    db.query(models.Workout).filter(models.Workout.id == workout_id).delete()

    db.commit()

@app.get("/api/news/{news_id}")
async def get_news_by_id(news_id: int, db: db_dependency):

    news_model = db.query(models.News).filter(models.News.id == news_id).first()

    if news_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"News of ID {news_id} Does not exist"
        )
    
    return news_model

@app.post("/api/news/new")
async def create_news(news: News, db: db_dependency):
    news_model = models.News()

    news_model.title = news.title
    news_model.body = news.body
    news_model.date = news.date
    
    db.add(news_model)
    db.commit()
    return news

@app.put("/api/workouts/{workout_id}")
async def update_news(news: News, news_id: int, db: db_dependency):
    news_model = db.query(models.News).filter(models.News.id == news_id).first()

    if news_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"News with ID {news_id} Does not exist"
        )
    
    news_model.title = news.title
    news_model.body = news.body
    news_model.date = news.date

    db.add(news_model)
    db.commit()
    return news

@app.delete("/api/news/{workout_id}")
async def delete_news(news_id: int, db: db_dependency):

    news_model = db.query(models.News).filter(models.News.id == news_id).first()

    if news_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"News with ID {news_id} Does not exist"
        )
    
    db.query(models.News).filter(models.News.id == news_id).delete()

    db.commit()

@app.get("/api/events/{event_id}")
async def get_event_by_id(event_id: int, db: db_dependency):

    event_model = db.query(models.Event).filter(models.Event.id == event_id).first()

    if event_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"Event of ID {event_id} Does not exist"
        )
    
    return event_model

@app.post("/api/events/new")
async def create_event(event: Event, db: db_dependency):
    event_model = models.Event()

    event_model.name = event.name
    event_model.description = event.description
    event_model.date = event.date

    db.add(event_model)
    db.commit()
    return event

@app.put("/api/events/{event_id}")
async def update_event(event: Event, event_id: int, db: db_dependency):
    event_model = db.query(models.Event).filter(models.Event.id == event_id).first()

    if event_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"Event with ID {event_id} Does not exist"
        )
    
    event_model.name = event.name
    event_model.description = event.description
    event_model.date = event.date

    db.add(event_model)
    db.commit()
    return event

@app.delete("/api/events/{event_id}")
async def delete_event(event_id: int, db: db_dependency):

    event_model = db.query(models.Event).filter(models.Event.id == event_id).first()

    if event_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"Event with ID {event_id} Does not exist"
        )
    
    db.query(models.Event).filter(models.Event.id == event_id).delete()

    db.commit()
