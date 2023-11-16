from datetime import timedelta, datetime
from validate import validate_card
from DB import get_db

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
db_dependency = Annotated[Session, Depends(get_db)]
# user_dependency = Annotated[dict, (Depends(get_current_user))]

class ProcessTransactionRequestBody(BaseModel):
    card_type: str
    card_number: str
    description: str
    amount: int

@router.post("/", status_code=status.HTTP_201_CREATED)
async def process_transaction(db: db_dependency, process_transaction_request_body: ProcessTransactionRequestBody):
    # Validate card first
    is_valid, message = validate_card(
        process_transaction_request_body.card_number, 
        process_transaction_request_body.card_type
    )
    
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    # If card is valid, process the transaction
    hashed_card_number = bcrypt_info.hash(process_transaction_request_body.card_number)
    new_transaction = Transactions(
        card_type=process_transaction_request_body.card_type,
        hashed_card_number=hashed_card_number,
        description=process_transaction_request_body.description,
        amount=process_transaction_request_body.amount,
        date=datetime.now()
    )

    db.add(new_transaction)
    db.commit()

    return {"success": True, "message": message}
    

@router.get("/", status_code=status.HTTP_200_OK)
async def get_transactions(db: db_dependency):
    return db.query(Transactions).all()
    
@router.patch("/transactions/{transaction_id}", status_code=status.HTTP_200_OK)
async def update_transaction_status(db: db_dependency, transaction_id: int, status: str):
    transaction = db.query(Transactions).filter(Transactions.id == transaction_id).first()
    if transaction:
        transaction.status = status
        db.commit()
        return {"success": True, "message": "Transaction status updated"}
    else:
        raise HTTPException(status_code=404, detail="Transaction not found")