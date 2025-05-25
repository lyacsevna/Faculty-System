from typing import Optional

from sqlalchemy.orm import Session

from ..models import models
from ..models.models import *
from ..schemas import schemas
from ..schemas.schemas import *

# Faculty CRUD
def get_faculty(db: Session, faculty_id: int):
    return db.query(models.Faculty).filter(models.Faculty.id == faculty_id).first()

def get_faculties(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Faculty).offset(skip).limit(limit).all()

def create_faculty(db: Session, faculty: schemas.FacultyCreate):
    db_faculty = models.Faculty(name=faculty.name)
    db.add(db_faculty)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty

def update_faculty(db: Session, faculty_id: int, faculty: schemas.FacultyUpdate):
    db_faculty = db.query(models.Faculty).filter(models.Faculty.id == faculty_id).first()
    if db_faculty:
        db_faculty.name = faculty.name
        db.commit()
        db.refresh(db_faculty)
    return db_faculty

def delete_faculty(db: Session, faculty_id: int):
    db_faculty = db.query(models.Faculty).filter(models.Faculty.id == faculty_id).first()
    if db_faculty:
        db.delete(db_faculty)
        db.commit()
        return True
    return False


# Program CRUD
def get_program(db: Session, program_id: int):
    return db.query(models.Program).filter(models.Program.id == program_id).first()


def get_programs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Program).offset(skip).limit(limit).all()


def create_program(db: Session, program: schemas.ProgramCreate):
    db_program = models.Program(**program.model_dump())
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program


def update_program(db: Session, program_id: int, program: schemas.ProgramUpdate):
    db_program = db.query(models.Program).filter(models.Program.id == program_id).first()
    if db_program:
        for key, value in program.model_dump().items():
            setattr(db_program, key, value)
        db.commit()
        db.refresh(db_program)
    return db_program


def delete_program(db: Session, program_id: int):
    db_program = db.query(models.Program).filter(models.Program.id == program_id).first()
    if db_program:
        db.delete(db_program)
        db.commit()
        return True
    return False


# Group CRUD
def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()


def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Group).offset(skip).limit(limit).all()


def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(**group.model_dump())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def update_group(db: Session, group_id: int, group: schemas.GroupUpdate):
    db_group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if db_group:
        for key, value in group.model_dump().items():
            setattr(db_group, key, value)
        db.commit()
        db.refresh(db_group)
    return db_group


def delete_group(db: Session, group_id: int):
    db_group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if db_group:
        db.delete(db_group)
        db.commit()
        return True
    return False


# Student CRUD
def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_student(db: Session, student_id: int, student: schemas.StudentUpdate):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student:
        for key, value in student.model_dump().items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False


# Добавим в Faculty CRUD
def get_faculty_programs(db: Session, faculty_id: int):
    return db.query(models.Program).filter(models.Program.faculty_id == faculty_id).all()


# Добавим в Program CRUD
def get_program_groups(db: Session, program_id: int):
    return db.query(models.Group).filter(models.Group.program_id == program_id).all()


# Добавим в Group CRUD
def get_group_students(db: Session, group_id: int,
                       budget_contract: Optional[str] = None,
                       status: Optional[str] = None,
                       gender: Optional[str] = None):
    query = db.query(models.Student).filter(models.Student.group_id == group_id)

    if budget_contract:
        query = query.filter(models.Student.budget_contract == budget_contract)
    if status:
        query = query.filter(models.Student.status == status)
    if gender:
        query = query.filter(models.Student.gender == gender)

    return query.all()