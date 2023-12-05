import re
from fastapi import HTTPException, status

def validate_password_length(password: str) -> None:
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long."
        )

def validate_password_content(password: str) -> None:
    if not re.match("^[A-Za-z0-9!@#$%^&*()_+=-]{8,}$", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain only numbers, letters, and special characters."
        )
        
def validate_email_presence(email: str) -> None:
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required."
        )

def validate_email_format(email: str) -> None:
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format."
        )