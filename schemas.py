from pydantic import BaseModel

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    course: str

    class Config:
        from_attributes = True

class Student(BaseModel):
    name: str
    age: int
    course: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str