from fastapi import FastAPI

from models import models
from db.database import engine
from routers import auth, admin, transactions

from fastapi.middleware.cors import CORSMiddleware


# application
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# sets up database defined in engine
models.Base.metadata.create_all(bind=engine)

# Set API endpoints on router
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(admin.router)
