from db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime



class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    
    first_name = Column(String)
    surname = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
  

class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    card_type = Column(String)
    hashed_card_number = Column(String)
    description = Column(String)
    amount = Column(Integer)
    complete = Column(Boolean, default=False)
    # owner_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime)










