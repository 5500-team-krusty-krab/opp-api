"""Authentication router for handling user signup and login."""
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from backend.helper import *
from backend.models.models import Users
from backend.DB import get_db
from backend.db.database import SessionLocal
from passlib.context import CryptContext
from typing import Annotated

router = APIRouter(tags=['auth'])

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')
# SECRET_KEY = secrets.token_urlsafe(32)
SECRET_KEY = "klajsdfkl;asjdflkjsadfklasdflk"
ALGORITHM = "HS256"

db_dependency = Annotated[Session, Depends(get_db)]

class UserSignupParam(BaseModel):
    """Parameters required for user signup."""
    name:str
    email: str
    password: str

@router.post("/signup")
async def user_signup(param: UserSignupParam, db: db_dependency):
    """
    Endpoint for user signup.

    :param param: UserSignupParam - Signup details.
    :param db: DbDependency - Database session dependency.
    :return: Dict indicating success status.
    """
    validate_email_presence(param.email)
    validate_email_format(param.email)
    validate_password_length(param.password)
    validate_password_content(param.password)

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
    """Parameters required for user login."""
    email: str
    password: str

@router.post("/login")
async def user_login(param: UserLoginParam, db: db_dependency):
    """
    Endpoint for user login.

    :param param: UserLoginParam - Login details.
    :param db: DbDependency - Database session dependency.
    :return: Dict with login message and access token.
    """
    

    user = authenticate_user(param.email, param.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect login details")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"userId": user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "message": "Successfully logged in",
        "access_token": access_token
    }
    

def authenticate_user(email: str, password: str, db: Session):
    """
    Authenticate user by email and password.

    :param email: str - User email.
    :param password: str - User password.
    :param db: Session - Database session.
    :return: User object or False.
    """
    user = db.query(Users).filter(
        Users.email == email,
    ).first()
    
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token.

    :param data: dict - Data to encode in the token.
    :param expires_delta: timedelta - Token expiry duration.
    :return: str - Encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db: db_dependency):
    """
    Get the current user based on the JWT token.

    :param token: Annotated[str, Depends(oauth2_bearer)] - JWT token.
    :param db: DbDependency - Database session dependency.
    :return: User object.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userId: str = payload.get('userId')
        if userId is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        return db.query(Users).get(userId)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')