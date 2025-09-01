from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import sessionmaker, declarative_base

engine = create_engine('sqlite:///./database.db')

session = sessionmaker(bind=engine)

base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()