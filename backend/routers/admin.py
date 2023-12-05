from typing import Annotated
from DB import get_db
from helper import *
# ... (other imports and code)

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session

from models.models import Users
from db.database import SessionLocal

router = APIRouter(prefix='/admin', tags=['admin'])

# Test
@router.get("/")
async def testRouter(db: Session = Depends(get_db)):
    return {"Hello": "World"}

# Dependency to ensure the current user is authenticated
def get_current_admin_user(db: Session = Depends(get_db)):
    # For simplicity, we are going to assume that the user with ID 1 is the admin
    admin_user_id = 1  # This should be the actual admin user ID in the database
    admin_user = db.query(Users).filter(Users.id == admin_user_id).first()
    if not admin_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin user not found")
    if admin_user.role.lower() != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not an admin")
    
    return admin_user

# Deactivate a user's account
@router.post("/users/{user_id}/deactivate")
async def deactivate_user(user_id: int, db: Session = Depends(get_db), admin: Users = Depends(get_current_admin_user)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_active = False
    db.commit()
    return {"ok": True, "message": "User deactivated successfully"}

# Read all user's information in the database
@router.get("/users")
async def read_all_users(db: Session = Depends(get_db), admin: Users = Depends(get_current_admin_user)):
    users = db.query(Users).all()
    return users