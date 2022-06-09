import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# to connect to DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

print("MODE -----------------------")
print(f"DEBUG: {os.getenv('DEBUG')}")

if os.getenv('DEBUG') == "true":
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    db = os.getenv("POSTGRES_DB")

    engine = create_engine(
        f"postgresql://{user}:{password}@postgres_db_container:5432/{db}"
        )

# create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
