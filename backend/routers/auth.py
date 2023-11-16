
import secrets
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from models.models import Users
from DB import get_db
from db.database import SessionLocal
from passlib.context import CryptContext
from typing import Annotated

router = APIRouter(prefix='/auth', tags=['auth'])

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"

db_dependency = Annotated[Session, Depends(get_db)]

class UserSignupParam(BaseModel):
    name:str
    email: str
    password: str

@router.post("/signup")
async def user_signup(param: UserSignupParam, db = db_dependency):

    #TODO validate email format
    # if invalid email format
    # raise HTTP ("invalid email")

    existing_user = db.query(Users).filter(
        Users.email == param.email,
    ).first()
    

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already in use."
        )
    
    user = Users(
        name = param.name,
        email = param.email,
        hashed_password = bcrypt_context.hash(param.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"success":True}

class UserLoginParam(BaseModel):
    email: str
    password: str

@router.post("/login")
async def user_login(param: UserLoginParam, db: db_dependency):
    

    user = authenticate_user(param.email, param.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect login details")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"email": user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
    

def authenticate_user(email: str, password: str, db: Session):
    user = db.query(Users).filter(
        Users.email == email,
    ).first()
    
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
