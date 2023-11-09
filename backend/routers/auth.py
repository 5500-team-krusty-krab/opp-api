
import secrets
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from models.models import Users
from db.database import SessionLocal
from passlib.context import CryptContext

router = APIRouter(prefix='/auth', tags=['auth'])

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Depends(get_db)

class UserRegistration(BaseModel):
    first_name: str
    last_name: str
    password: str
    role: str

class TokenData(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=TokenData)
async def register_user(user_data: UserRegistration, db: Session = db_dependency):
    existing_user = db.query(Users).filter(
        Users.first_name == user_data.first_name,
        Users.surname == user_data.last_name
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with given name already exists."
        )
    
    user = Users(
        first_name=user_data.first_name,
        surname=user_data.last_name,
        role=user_data.role,
        hashed_password=bcrypt_context.hash(user_data.password),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": f"{user.first_name} {user.surname}", "id": user.id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=TokenData)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect login details")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": f"{user.first_name} {user.surname}", "id": user.id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

def authenticate_user(first_name: str, last_name: str, password: str, db: Session):
    user = db.query(Users).filter(
        Users.first_name == first_name,
        Users.surname == last_name
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
