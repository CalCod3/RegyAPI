from db.schemas import CreateUserRequest, Token
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from datetime import timedelta, datetime
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Annotated
from security import authenticate_user, create_access_token
from starlette import status
from db.database import Base, SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from db.models import User, Box
import os


router = APIRouter(
    prefix = '/auth',
    tags = ['auth']
)

db_dependency = Annotated[Session,  Depends(get_db)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(
        box_id=create_user_request.box_id,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        email=create_user_request.email,
        password_hash=bcrypt_context.hash(create_user_request.password)
    )
    db.add(create_user_model)
    db.commit()

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    
    token = create_access_token(user.email, user.id, expires_delta=timedelta(minutes=30))

    return {'access_token': token, 'token_type': 'bearer'}
