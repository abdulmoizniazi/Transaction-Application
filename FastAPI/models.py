from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, Date


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    category = Column(String)
    description = Column(String)
    is_income = Column(Boolean)
    date = Column(Date)

    
# sqlmodel

# from sqlmodel import SQLModel, Field
# from datetime import date


# class Transaction(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     amount: float
#     category: str
#     description: str
#     is_income: bool
#     date: date
