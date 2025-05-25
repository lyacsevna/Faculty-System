from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models
from .crud import crud
from .database import SessionLocal, engine
from .schemas.schemas import (
    Faculty, FacultyCreate,
    Program, ProgramCreate,
    Group, GroupCreate,
    Student, StudentCreate, StudentUpdate, GroupUpdate, ProgramUpdate, FacultyUpdate
)
from .crud.crud import (
    get_faculties, create_faculty,
    get_programs, create_program,
    get_groups, create_group,
    get_students, create_student
)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Faculty endpoints
@app.post("/faculties/", response_model=Faculty, status_code=status.HTTP_201_CREATED)
def create_faculty(faculty: FacultyCreate, db: Session = Depends(get_db)):
    return crud.create_faculty(db=db, faculty=faculty)

@app.get("/faculties/", response_model=list[Faculty])
def read_faculties(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_faculties(db, skip=skip, limit=limit)

@app.put("/faculties/{faculty_id}", response_model=Faculty)
def update_faculty(faculty_id: int, faculty: FacultyUpdate, db: Session = Depends(get_db)):
    updated_faculty = crud.update_faculty(db=db, faculty_id=faculty_id, faculty=faculty)
    if not updated_faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return updated_faculty

@app.delete("/faculties/{faculty_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faculty(faculty_id: int, db: Session = Depends(get_db)):
    if not crud.delete_faculty(db=db, faculty_id=faculty_id):
        raise HTTPException(status_code=404, detail="Faculty not found")

# Program endpoints
@app.post("/programs/", response_model=Program, status_code=status.HTTP_201_CREATED)
def create_program(program: ProgramCreate, db: Session = Depends(get_db)):
    return crud.create_program(db=db, program=program)

@app.get("/programs/", response_model=list[Program])
def read_programs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_programs(db, skip=skip, limit=limit)

@app.put("/programs/{program_id}", response_model=Program)
def update_program(program_id: int, program: ProgramUpdate, db: Session = Depends(get_db)):
    updated_program = crud.update_program(db=db, program_id=program_id, program=program)
    if not updated_program:
        raise HTTPException(status_code=404, detail="Program not found")
    return updated_program

@app.delete("/programs/{program_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_program(program_id: int, db: Session = Depends(get_db)):
    if not crud.delete_program(db=db, program_id=program_id):
        raise HTTPException(status_code=404, detail="Program not found")

# Group endpoints
@app.post("/groups/", response_model=Group, status_code=status.HTTP_201_CREATED)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    return crud.create_group(db=db, group=group)

@app.get("/groups/", response_model=list[Group])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_groups(db, skip=skip, limit=limit)

@app.put("/groups/{group_id}", response_model=Group)
def update_group(group_id: int, group: GroupUpdate, db: Session = Depends(get_db)):
    updated_group = crud.update_group(db=db, group_id=group_id, group=group)
    if not updated_group:
        raise HTTPException(status_code=404, detail="Group not found")
    return updated_group

@app.delete("/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    if not crud.delete_group(db=db, group_id=group_id):
        raise HTTPException(status_code=404, detail="Group not found")

# Student endpoints
@app.post("/students/", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db=db, student=student)

@app.get("/students/", response_model=list[Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_students(db, skip=skip, limit=limit)

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    updated_student = crud.update_student(db=db, student_id=student_id, student=student)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    if not crud.delete_student(db=db, student_id=student_id):
        raise HTTPException(status_code=404, detail="Student not found")