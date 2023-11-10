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

router = APIRouter(prefix='/transactions', tags=['transactions'])

import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

bcrypt_info = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
# user_dependency = Annotated[dict, (Depends(get_current_user))]

class ProcessTransactionRequestBody(BaseModel):
    card_type: str
    card_number: str
    description: str
    amount: int


@router.post("/", status_code=status.HTTP_201_CREATED)
async def process_transaction(db: db_dependency, process_transaction_request_body: ProcessTransactionRequestBody):

    process_transaction = Transactions(
        card_type=process_transaction_request_body.card_type,
        hashed_card_number=bcrypt_info.hash(process_transaction_request_body.card_number), #will implement irreversible encryption next milestone
        description=process_transaction_request_body.description,
        amount=process_transaction_request_body.amount,
        complete=False, #TODO: if debit: True, if credit: False
        date = datetime.now()
    )

    db.add(process_transaction)
    db.commit()

    return {"success":True}

@router.get("/", status_code=status.HTTP_200_OK)
async def get_transactions(db: db_dependency):
    return db.query(Transactions).all()

