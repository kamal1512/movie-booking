"""---------------------------BEFORE DOCKER--------------------------"""

# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base
#
# DATABASE_URL = "postgresql://postgres:root@localhost:5432/movie_booking"
#
# engine = create_engine(
#     DATABASE_URL,
#     echo=True
# )
#
# Base = declarative_base()       # Base to create table

"""---------------------------AFTER DOCKER--------------------------"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()       # Base to create table
