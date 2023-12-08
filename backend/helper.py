# helper.py: Contains helper functions for validating user input in a FastAPI application.

import re
from fastapi import HTTPException, status

def validate_password_length(password: str) -> None:
    """
    Validates the length of a password.

    :param password: The password to be validated.
    :raise HTTPException: If the password is shorter than 8 characters.
    """
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long."
        )

def validate_password_content(password: str) -> None:
    """
    Validates the content of a password.

    :param password: The password to be validated.
    :raise HTTPException: If the password doesn't match the required pattern.
    """
    if not re.match("^[A-Za-z0-9!@#$%^&*()_+=-]{8,}$", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain only numbers, letters, and special characters."
        )

def validate_email_presence(email: str) -> None:
    """
    Checks if the email is provided.

    :param email: The email to be validated.
    :raise HTTPException: If the email is empty.
    """
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required."
        )

def validate_email_format(email: str) -> None:
    """
    Validates the format of an email.

    :param email: The email to be validated.
    :raise HTTPException: If the email format is invalid.
    """
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format."
        )
    
# def check_positive_amount(amount):
#     if amount <=0:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Please enter a positive amount."
#         )
