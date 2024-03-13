import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from datetime import timedelta, datetime
from passlib.context import CryptContext
from db.models import User, Box
from starlette import status
from jose import JWTError, jwt


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def hash_password(password: str):
    return bcrypt_context.hash(password)

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
        payload: jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
        email: str = payload.get('sub')
        id: int = payload.get('id')

        if email is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        return {'email': email, 'id': id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    