from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'sqlite:///./finance.db'

engine = create_engine(URL_DATABASE, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# sqlmodel

# from sqlmodel import SQLModel, create_engine, Session

# # SQLite DB URL
# URL_DATABASE = 'sqlite:///./finance.db'

# # Create engine
# engine = create_engine(URL_DATABASE, connect_args={"check_same_thread": False})

# # Session
# def get_session():
#     with Session(engine) as session:
#         yield session

# # Create all tables (typically called once)
# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)
