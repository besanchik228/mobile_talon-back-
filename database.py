from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

engine = create_engine(os.getenv("data_adress"))

session = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()