# admin.py: Router for admin-related operations in a FastAPI application

from typing import Annotated
from DB import get_db
from helper import *


from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session

from models.models import Users
from db.database import SessionLocal




router = APIRouter(prefix='/admin', tags=['admin'])

@router.get("/")
async def test_router():
    """
    Test endpoint to verify that the router is functioning correctly.
    """
    return {"Hello": "World"}

def get_current_admin_user(db: Session = Depends(get_db)) -> Users:
    """
    Dependency to ensure the current user is authenticated and is an admin.
    Retrieves the admin user from the database.
    """
    admin_user_id = 1  # Replace with actual admin user ID
    admin_user = db.query(Users).filter(Users.id == admin_user_id).first()
    if not admin_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Admin user not found")
    if admin_user.role.lower() != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="User is not an admin")
    return admin_user

@router.post("/users/{user_id}/deactivate")
async def deactivate_user(user_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Deactivate a user's account. Only accessible by admin users.
    """
    _ = get_current_admin_user(db)  # Ensure current user is admin
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User not found")

    user.is_active = False
    db.commit()
    return {"ok": True, "message": "User deactivated successfully"}

@router.get("/users")
async def read_all_users(db: Session = Depends(get_db)) -> list:
    """
    Retrieve all user information from the database. Only accessible by admin users.
    """
    _ = get_current_admin_user(db)  # Ensure current user is admin
    users = db.query(Users).all()
    return users
