# transactions.py: Defines routes and logic for transaction-related operations in a FastAPI application.

import os
import re
from datetime import datetime, timedelta
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from models.models import Transactions, TransactionStatus
from validate import validate_card
from check_fund import check_fund_card
from db.database import get_db
from routers.auth import get_current_user

load_dotenv()  # Load environment variables from .env file.

router = APIRouter(prefix='/transactions', tags=['transactions'])
bcrypt_info = CryptContext(schemes=['bcrypt'], deprecated='auto')

DbDependency = Annotated[Session, Depends(get_db)]
UserDependency = Annotated[dict, Depends(get_current_user)]


class ProcessTransactionRequestBody(BaseModel):
    """
    Request body schema for processing a transaction.
    """
    card_type: str
    card_number: str
    description: str
    amount: int

@router.post("/new", status_code=status.HTTP_201_CREATED)
async def process_transaction(db: DbDependency, 
                              process_transaction_request_body: ProcessTransactionRequestBody, 
                              user: UserDependency) -> dict:
    """
    Process a new transaction based on the provided request body and user details.
    """
    # Validate card first
    is_valid, message = validate_card(
        process_transaction_request_body.card_number, 
        process_transaction_request_body.card_type
    )
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    # Check if sufficient funds are available
    is_sufficient, message = check_fund_card(
        process_transaction_request_body.card_number, 
        process_transaction_request_body.card_type,
        process_transaction_request_body.amount
    )
    if not is_sufficient:
        return {"success": False, "message": message}

    # Process transaction
    new_transaction = Transactions(
        card_type=process_transaction_request_body.card_type,
        card_number=process_transaction_request_body.card_number[-4:],
        description=process_transaction_request_body.description,
        amount=process_transaction_request_body.amount,
        date=datetime.now(),
        status=TransactionStatus.COMPLETED if process_transaction_request_body.card_type == 'debit' else TransactionStatus.PENDING,
        owner_id=user.id
    )
    db.add(new_transaction)
    db.commit()
    return {"success": True, "message": message}

@router.get("/", status_code=status.HTTP_200_OK)
async def get_transactions(db: DbDependency, user: UserDependency,
                           transaction_status: str = "completed",
                           start: str = None, 
                           end: str = None) -> dict:
    """
    Retrieve a list of transactions for the current user, filtered by status and date range.
    """
    update_status(db, user)
    status_value = TransactionStatus.PENDING if transaction_status == "pending" else TransactionStatus.COMPLETED
    query = db.query(Transactions).filter_by(owner_id=user.id, status=status_value).order_by(Transactions.date.desc())
    
    if start:
        start_date_time = datetime.strptime(start, "%Y-%m-%d").replace(hour=0, minute=0, second=0)
        query = query.filter(Transactions.date >= start_date_time)

    if end:
        end_date_time = datetime.strptime(end, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
        query = query.filter(Transactions.date <= end_date_time)

    transactions = query.all()
    balance = calculate_balance(transactions)
    return {"balance": balance, "transactions": transactions}

def update_status(db: DbDependency, user: UserDependency):
    """
    Update the status of pending transactions that have passed the 48-hour window.
    """
    db.query(Transactions)\
      .filter_by(owner_id=user.id, status=TransactionStatus.PENDING)\
      .filter(datetime.now() - timedelta(hours=48) >= Transactions.date)\
      .update({'status': TransactionStatus.COMPLETED})
    db.commit()

def calculate_balance(transactions: list) -> int:
    """
    Calculate the total balance from a list of transactions.
    """
    total = sum(transaction.amount for transaction in transactions)
    return total


