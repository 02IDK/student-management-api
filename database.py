from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

print(os.path.abspath("students.db"))

database_url="sqlite:///students.db"

engine=create_engine(database_url,connect_args={"check_same_thread": False})

SessionLocal=sessionmaker(autocommit=False,
                          autoflush=False,
                          bind=engine)
def get_db():
    db=SessionLocal()

    try:
        yield db

    finally:
        db.close()