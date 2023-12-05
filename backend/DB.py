"""Module for database session handling."""

from db.database import SessionLocal

def get_db():
    """
    Create a new database session and handle its closure after use.
    
    Yields:
        db: SQLAlchemy session object that is used to interact with the database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
