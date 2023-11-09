from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from starlette import status

from models.models import *
from passlib.context import CryptContext
from db.database import SessionLocal
from typing import Annotated, Any
from sqlalchemy.orm import Session
from jose import jwt, JWTError

router = APIRouter(prefix='/auth', tags=['auth'])

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Depends(get_db)

class UserRegistration(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    user_role: str

class TokenData(BaseModel):
    access_token: str
    token_type: str

@router.post("/")
async def register_user(user_data: UserRegistration, db: Session = db_dependency):
    user = Users(
        email=user_data.email,
        username=user_data.username,
        first_name=user_data.first_name,
        surname=user_data.last_name,
        role=user_data.user_role,
        hashed_password=bcrypt_context.hash(user_data.password),
        is_active=True
    )
    db.add(user)
    db.commit()

@router.post("/token", response_model=TokenData)
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = db_dependency):
    user = verify_credentials(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token_expires = timedelta(minutes=30)
    token = create_jwt_token(user.username, user.id, user.role, token_expires)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
async def login(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    
    token_expires = timedelta(minutes=30)
    token = create_jwt_token(user.username, user.id, user.role, token_expires)
    return {"access_token": token, "token_type": "bearer"}

def verify_credentials(username: str, password: str, db: Session) -> Users:
    user = db.query(Users).filter(Users.username == username).first()
    if not user or not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_jwt_token(username: str, user_id: int, role: str, expires_delta: timedelta) -> str:
    data_to_encode = {"sub": username, "id": user_id, "role": role}
    expiration = datetime.utcnow() + expires_delta
    data_to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(data_to_encode, 'YOUR_SECRET_KEY', algorithm='HS256')
    return encoded_jwt