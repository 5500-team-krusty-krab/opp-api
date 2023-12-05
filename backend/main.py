# main.py: Main application module for a FastAPI application, setting up routes and middleware.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import models
from db.database import engine
from routers import auth, admin, transactions

# Create the FastAPI application instance
app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database
models.Base.metadata.create_all(bind=engine)

# Include routers for different parts of the application
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    """
    Root endpoint that returns a simple success message.
    Useful for verifying if the application is running correctly.
    """
    return {"Docker": "Success"}

