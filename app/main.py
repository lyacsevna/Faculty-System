from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from starlette.middleware.cors import CORSMiddleware

from .import database
from .models.models import (
    Faculty,
    Program,
    Group,
    Student
)

from .schemas.schemas import (
    FacultyCreate,
    GroupCreate,
    StudentCreate,
    ProgramCreate
)

from .crud.crud import (
    get_faculties, create_faculty, get_faculty, update_faculty, delete_faculty,
    get_programs, create_program, get_program, update_program, delete_program,
    get_groups, create_group, get_group, update_group, delete_group,
    get_students, create_student, get_student, update_student, delete_student
)


app = FastAPI()
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,  # Allow credentials such as cookies
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allow all headers
)
# Faculty endpoints
@app.post("/faculties/", response_model=Faculty)
def create_new_faculty(faculty: FacultyCreate, db: Session = Depends(database.get_db)):
    return create_faculty(db=db, faculty=faculty)

@app.get("/faculties/", response_model=List[Faculty])
def read_faculties(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    faculties = get_faculties(db, skip=skip, limit=limit)
    return faculties

@app.get("/faculties/{faculty_id}", response_model=Faculty)
def read_faculty(faculty_id: int, db: Session = Depends(database.get_db)):
    db_faculty = get_faculty(db, faculty_id=faculty_id)
    if db_faculty is None:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return db_faculty

@app.put("/faculties/{faculty_id}", response_model=Faculty)
def update_existing_faculty(faculty_id: int, faculty_update: Dict[str, Any], db: Session = Depends(database.get_db)):
    db_faculty = update_faculty(db, faculty_id=faculty_id, faculty_update=faculty_update)
    if db_faculty is None:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return db_faculty

@app.delete("/faculties/{faculty_id}")
def remove_faculty(faculty_id: int, db: Session = Depends(database.get_db)):
    success = delete_faculty(db, faculty_id=faculty_id)
    if not success:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return {"message": "Faculty deleted successfully"}

# Program endpoints
@app.post("/programs/", response_model=Program)
def create_new_program(program: ProgramCreate, db: Session = Depends(database.get_db)):
    return create_program(db=db, program=program)

@app.get("/programs/", response_model=List[Program])
def read_programs(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    programs = get_programs(db, skip=skip, limit=limit)
    return programs

@app.get("/programs/{program_id}", response_model=Program)
def read_program(program_id: int, db: Session = Depends(database.get_db)):
    db_program = get_program(db, program_id=program_id)
    if db_program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    return db_program

@app.put("/programs/{program_id}", response_model=Program)
def update_existing_program(program_id: int, program_update: Dict[str, Any], db: Session = Depends(database.get_db)):
    db_program = update_program(db, program_id=program_id, program_update=program_update)
    if db_program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    return db_program

@app.delete("/programs/{program_id}")
def remove_program(program_id: int, db: Session = Depends(database.get_db)):
    success = delete_program(db, program_id=program_id)
    if not success:
        raise HTTPException(status_code=404, detail="Program not found")
    return {"message": "Program deleted successfully"}

# Group endpoints
@app.post("/groups/", response_model=Group)
def create_new_group(group: GroupCreate, db: Session = Depends(database.get_db)):
    return create_group(db=db, group=group)

@app.get("/groups/", response_model=List[Group])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    groups = get_groups(db, skip=skip, limit=limit)
    return groups

@app.get("/groups/{group_id}", response_model=Group)
def read_group(group_id: int, db: Session = Depends(database.get_db)):
    db_group = get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

@app.put("/groups/{group_id}", response_model=Group)
def update_existing_group(group_id: int, group_update: Dict[str, Any], db: Session = Depends(database.get_db)):
    db_group = update_group(db, group_id=group_id, group_update=group_update)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

@app.delete("/groups/{group_id}")
def remove_group(group_id: int, db: Session = Depends(database.get_db)):
    success = delete_group(db, group_id=group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Group not found")
    return {"message": "Group deleted successfully"}

# Student endpoints
@app.post("/students/", response_model=Student)
def create_new_student(student: StudentCreate, db: Session = Depends(database.get_db)):
    return create_student(db=db, student=student)

@app.get("/students/", response_model=List[Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    students = get_students(db, skip=skip, limit=limit)
    return students

@app.get("/students/{student_id}", response_model=Student)
def read_student(student_id: int, db: Session = Depends(database.get_db)):
    db_student = get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.put("/students/{student_id}", response_model=Student)
def update_existing_student(student_id: int, student_update: Dict[str, Any], db: Session = Depends(database.get_db)):
    db_student = update_student(db, student_id=student_id, student_update=student_update)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.delete("/students/{student_id}")
def remove_student(student_id: int, db: Session = Depends(database.get_db)):
    success = delete_student(db, student_id=student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}