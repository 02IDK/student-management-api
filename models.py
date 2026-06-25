from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import declarative_base

Base=declarative_base()

class StudentDB(Base):
    __tablename__="students"

    id=Column(Integer, primary_key=True, index=True)
    name=Column(String)
    age=Column(Integer)
    course=Column(String)
    
class UserDB(Base):
    __tablename__="users"

    id=Column(Integer, primary_key=True, index=True)
    username=Column(String, unique=True, nullable=False)
    password=Column(String, nullable=False)
