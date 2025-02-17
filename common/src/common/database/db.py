import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if not (DATABASE_URL := os.getenv("SQLALCHEMY_DATABASE_URL")):
    raise ValueError("SQLALCHEMY_DATABASE_URL environment variable must be set")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
