import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

SQL_ALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as db:
        yield db