from typing import Annotated
from db.database import get_db
from db.schemas import Attendance, Box, Event, News, Workout
from fastapi import Depends, APIRouter, HTTPException
import db.models as models
from sqlalchemy.orm import Session



router = APIRouter(
    prefix = '/admin',
    tags = ['admin']
)

db_dependency = Annotated[Session,  Depends(get_db)]

@router.post("/boxes/new")
async def create_box(box: Box, db: db_dependency):
    box_model = models.Box()

    box_model.name = box.name  # type: ignore

    db.add(box_model)
    db.commit()
    return box

@router.get("/boxes")
async def get_boxes(db: db_dependency):
    return db.query(models.Box).all()
    

@router.put("/boxes/{box_id}")
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

@router.delete("/boxes/{box_id}")
async def delete_box(box_id: int, db: db_dependency):

    box_model = db.query(models.Box).filter(models.Box.id == box_id).first()

    if box_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"Box with ID {box_id} Does not exist"
        )
    
    db.query(models.Box).filter(models.Box.id == box_id).delete()

    db.commit()

@router.post("/attendance/new")
async def create_attendance(classroom: Attendance, db: db_dependency):
    class_model = models.Attendance()

    class_model.date = classroom.date  # type: ignore
    class_model.owner_id = classroom.owner_id

    db.add(class_model)
    db.commit()
    return classroom

@router.delete("/attendance/{user_id}")
async def delete_attendance(user_id: int, db: db_dependency):

    class_model = db.query(models.Attendance).filter(models.Attendance.user_id == user_id).first()

    if class_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"Attendance for user with ID {user_id} Does not exist"
        )
    
    db.query(models.Attendance).filter(models.Attendance.user_id == user_id).delete()

    db.commit()

@router.post("/workouts/new")
async def create_workout(workout: Workout, db: db_dependency):
    workout_model = models.Workout()

    workout_model.name = workout.name
    workout_model.type = workout.type
    workout_model.date = workout.date
    workout_model.time = workout.time 

    db.add(workout_model)
    db.commit()
    return workout

@router.put("/workouts/{workout_id}")
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

@router.delete("/workouts/{workout_id}")
async def delete_workout(workout_id: int, db: db_dependency):

    workout_model = db.query(models.Workout).filter(models.Workout.id == workout_id).first()

    if workout_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"Workout with ID {workout_id} Does not exist"
        )
    
    db.query(models.Workout).filter(models.Workout.id == workout_id).delete()

    db.commit()
@router.post("/news/new")
async def create_news(news: News, db: db_dependency):
    news_model = models.News()

    news_model.title = news.title
    news_model.body = news.body
    news_model.date = news.date
    
    db.add(news_model)
    db.commit()
    return news

@router.put("/workouts/{news_id}")
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

@router.delete("/news/{news_id}")
async def delete_news(news_id: int, db: db_dependency):

    news_model = db.query(models.News).filter(models.News.id == news_id).first()

    if news_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"News with ID {news_id} Does not exist"
        )
    
    db.query(models.News).filter(models.News.id == news_id).delete()

    db.commit()

@router.post("/events/new")
async def create_event(event: Event, db: db_dependency):
    event_model = models.Event()

    event_model.name = event.name
    event_model.description = event.description
    event_model.date = event.date

    db.add(event_model)
    db.commit()
    return event

@router.put("/events/{event_id}")
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

@router.delete("/events/{event_id}")
async def delete_event(event_id: int, db: db_dependency):

    event_model = db.query(models.Event).filter(models.Event.id == event_id).first()

    if event_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"Event with ID {event_id} Does not exist"
        )
    
    db.query(models.Event).filter(models.Event.id == event_id).delete()

    db.commit()
