from datetime import timedelta, datetime
from validate import validate_card
from DB import get_db
from check_fund import check_fund_card

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from starlette import status

from models.models import *
from passlib.context import CryptContext
from db.database import SessionLocal
from typing import Annotated, Any
from sqlalchemy.orm import Session
# from jose import jwt, JWTError

from routers.auth import get_current_user

router = APIRouter(prefix='/transactions', tags=['transactions'])

import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

bcrypt_info = CryptContext(schemes=['bcrypt'], deprecated='auto')
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, (Depends(get_current_user))]

class ProcessTransactionRequestBody(BaseModel):
    card_type: str
    card_number: str
    description: str
    amount: int

@router.post("/", status_code=status.HTTP_201_CREATED)
async def process_transaction(db: db_dependency, process_transaction_request_body: ProcessTransactionRequestBody, user:user_dependency):
    

    # Validate card first
    is_valid, message = validate_card(
        process_transaction_request_body.card_number, 
        process_transaction_request_body.card_type
    )

    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    is_sufficient, message = check_fund_card(
        process_transaction_request_body.card_number, 
        process_transaction_request_body.card_type,
        process_transaction_request_body.amount
    )
    if not is_sufficient:
        return {"success": False, "message": message}
    

    # If card is valid, process the transaction
    hashed_card_number = bcrypt_info.hash(process_transaction_request_body.card_number)
    new_transaction = Transactions(
        card_type=process_transaction_request_body.card_type,
        hashed_card_number=hashed_card_number,
        description=process_transaction_request_body.description,
        amount=process_transaction_request_body.amount,
        date=datetime.now(),
        status=TransactionStatus.COMPLETED if process_transaction_request_body.card_type == 'debit' else TransactionStatus.PENDING,
        owner_id = user.id
    )
 
    db.add(new_transaction)
    db.commit()

    return {"success": True, "message": message}
    



@router.get("/", status_code=status.HTTP_200_OK)
async def get_transactions(db: db_dependency, user: user_dependency):
    pending_transactions = db.query(Transactions)\
        .filter_by(owner_id=user.id, card_type='credit', status=TransactionStatus.PENDING)\
        .all()

    for transaction in pending_transactions:
        if datetime.now() >= transaction.pending_time + timedelta(hours=48):  
            transaction.status = TransactionStatus.APPROVED
            transaction.approved_time = datetime.now()

    db.commit()  

   
    return db.query(Transactions).filter_by(owner_id=user.id).all()