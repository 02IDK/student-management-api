from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from database import engine, get_db
from models import Base, StudentDB, UserDB
from schemas import Student, UserLogin, UserCreate, StudentResponse
from auth import hash_password, verify_password, create_access_token,verify_token
from typing import List
from datetime import datetime
from time import time

security=HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token=credentials.credentials
    username=verify_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail="Invalid Token")
    
    return username

app = FastAPI(
    title="Student Management API",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

@app.middleware("http")
async def log_requests(request, call_next):
    
    start = time()
    response = await call_next(request)
    duration = time() - start

    print(f"{datetime.now()} |" f"{request.method} |" f"{request.url.path}" f"took{duration:.4f}s")

    return response


# Home Route
@app.get("/")
def home():
    return {"message": "Student Management API Running"}

#authentication
@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user=(db.query(UserDB).filter(UserDB.username == user.username).first())

    if existing_user:
        raise HTTPException(status_code=400,detail="Username already exists")
    
    hashed_pw=hash_password(user.password)

    new_user=UserDB(username=user.username,password=hashed_pw)
    db.add(new_user)
    db.commit()

    return {"message":"User registered successfully"}

@app.post("/login")
def login(user: UserLogin,db: Session = Depends(get_db)):
    db_user=(db.query(UserDB).filter(UserDB.username== user.username).first())

    if not db_user:
        raise HTTPException(status_code=401, detail="INvalid username or password")
    
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token=create_access_token(data={"sub":db_user.username})

    return {"access_token":token,"token_type":"bearer"}
   

# Create Student
@app.post("/students")
def create_student(student: Student,db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):

    new_student = StudentDB(
        name=student.name,
        age=student.age,
        course=student.course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Student added successfully",
        "student_id": new_student.id
    }


# Get All Students
@app.get("/students", response_model=List[StudentResponse])
def get_students(db: Session = Depends(get_db)):

    students = db.query(StudentDB).all()

    return students


# Get One Student
@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int,db: Session = Depends(get_db)):

    student = (
        db.query(StudentDB)
        .filter(StudentDB.id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# Update Student
@app.put("/students/{student_id}")
def update_student(student_id: int,updated_student: Student,db: Session = Depends(get_db),
                   current_user: str = Depends(get_current_user)
):

    student = (
        db.query(StudentDB)
        .filter(StudentDB.id == student_id)
        .first()
    )

    if not student:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.name = updated_student.name
    student.age = updated_student.age
    student.course = updated_student.course

    db.commit()
    db.refresh(student)

    return {
        "message": "Student updated successfully"
    }


# Delete Student
@app.delete("/students/{student_id}")
def delete_student(student_id: int,db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):

    student = (
        db.query(StudentDB)
        .filter(StudentDB.id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully"
    }