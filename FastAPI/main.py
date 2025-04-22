from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
from database import SessionLocal, engine
from typing import Annotated, List
from sqlalchemy.orm import Session
import models 

# from database import get_session, engine, create_db_and_tables
# from sqlmodel import Session

app = FastAPI()

origins = [
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
async def check():
    return {'message': "Hola Todos!"}


class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str
    is_income: bool
    date: date

class TransactionModel(TransactionBase):
    id: int

    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
# db_dependency = Annotated[Session, Depends(get_session)]


models.Base.metadata.create_all(bind=engine)
# create_db_and_tables()



# TransactionModel & TransactionBase ---> Transaction
@app.post('/transactions/', response_model=TransactionModel)
async def create_transaction(transaction: TransactionBase, db: db_dependency):
    db_transaction = models.Transaction(**transaction.model_dump()) # this line would be eliminated
    db.add(db_transaction)
    # db.add(transaction)
    db.commit()
    db.refresh(db_transaction)
    # db.refresh(transaction)
    return db_transaction
    # return transaction


# @app.get('/transactions/', response_model=List[Transaction])
@app.get('/transactions/', response_model=List[TransactionModel])
async def read_transactions(db: db_dependency, skip: int=0, limit: int=100):
    transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
    return transactions


@app.delete('/transactions/{transaction_id}')
async def delete_transaction(transaction_id: int, db: db_dependency):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(db_transaction)
    db.commit()
    return {'message': 'Transaction deleted successfully'}