from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer
from pathlib import Path

import os



path = Path("src/backend/.env")
load_dotenv(dotenv_path=path)

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DB_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autoflush=True, bind=engine)

Base = declarative_base()


class BaseModel(Base):

    __abstract__ = True
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():

    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(e)