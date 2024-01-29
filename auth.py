from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from datetime import timedelta, datetime
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Annotated
from starlette import status
from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session
from models import User, Box
import os
from dotenv import load_dotenv


router = APIRouter(
    prefix = '/auth',
    tags = ['auth']
)


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class Box(BaseModel):
    name: str

class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    box_id: int
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
     
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close() 

db_dependency = Annotated[Session,  Depends(get_db)]


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

def authenticate_user(email: str, password: str, db):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.password_hash):
        return False
    return user

def create_access_token(email: str, id: int, expires_delta: timedelta):
    encode = {'sub': email, 'id': id}
    expiry = datetime.utcnow() + expires_delta
    encode.update({'exp': expiry})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload: jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        id: int = payload.get('id')

        if email is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        return {'email': email, 'id': id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    