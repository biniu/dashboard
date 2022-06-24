import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from .config import get_config


settings = get_config(os.getenv("ENV") or "test")
SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.bind = engine


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


# to connect to DB
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# print("MODE -----------------------")
# print(f"DEBUG: {os.getenv('DEBUG')}")
#
# if os.getenv('DEBUG') == "true":
#     engine = create_engine(
#         SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
#     )
# else:
#     user = os.getenv("POSTGRES_USER")
#     password = os.getenv("POSTGRES_PASSWORD")
#     db = os.getenv("POSTGRES_DB")
#
#     engine = create_engine(
#         f"postgresql://{user}:{password}@postgres_db_container:5432/{db}"
#         )
#
# # create session
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()



