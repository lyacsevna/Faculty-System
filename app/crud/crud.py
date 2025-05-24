from typing import Dict, Any

from sqlalchemy.orm import Session

from ..models.models import Faculty, Program, Group, Student, FacultyCreate, ProgramCreate, GroupCreate, StudentCreate


# Faculty CRUD

def get_faculty(db: Session, faculty_id: int):
    return db.query(Faculty).filter(Faculty.id == faculty_id).first()


def get_faculties(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Faculty).offset(skip).limit(limit).all()


def create_faculty(db: Session, faculty: FacultyCreate):
    db_faculty = Faculty(name=faculty.name)
    db.add(db_faculty)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty

def update_faculty(db: Session, faculty_id: int, faculty_update: Dict[str, Any]):
    db_faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not db_faculty:
        return None
    for key, value in faculty_update.items():
        setattr(db_faculty, key, value)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty


def delete_faculty(db: Session, faculty_id: int):
    db_faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not db_faculty:
        return False
    db.delete(db_faculty)
    db.commit()
    return True

# Program CRUD


def get_program(db: Session, program_id: int):
    return db.query(Program).filter(Program.id == program_id).first()

def get_programs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Program).offset(skip).limit(limit).all()

def create_program(db: Session, program: ProgramCreate):
    db_program = Program(
        name=program.name,
        faculty_id=program.faculty_id,
        education_level=program.education_level
    )
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program

def update_program(db: Session, program_id: int, program_update: Dict[str, Any]):
    db_program = db.query(Program).filter(Program.id == program_id).first()
    if not db_program:
        return None
    for key, value in program_update.items():
        setattr(db_program, key, value)
    db.commit()
    db.refresh(db_program)
    return db_program


def delete_program(db: Session, program_id: int):
    db_program = db.query(Program).filter(Program.id == program_id).first()
    if not db_program:
        return False
    db.delete(db_program)
    db.commit()
    return True

# Group CRUD
def get_group(db: Session, group_id: int):
    return db.query(Group).filter(Group.id == group_id).first()

def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Group).offset(skip).limit(limit).all()

def create_group(db: Session, group: GroupCreate):
    db_group = Group(
        name=group.name,
        program_id=group.program_id,
        study_form=group.study_form,
        education_level=group.education_level
    )
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def update_group(db: Session, group_id: int, group_update: Dict[str, Any]):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if not db_group:
        return None
    for key, value in group_update.items():
        setattr(db_group, key, value)
    db.commit()
    db.refresh(db_group)
    return db_group

def delete_group(db: Session, group_id: int):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if not db_group:
        return False
    db.delete(db_group)
    db.commit()
    return True

# Student CRUD
def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Student).offset(skip).limit(limit).all()

def create_student(db: Session, student: StudentCreate):
    db_student = Student(
        last_name=student.last_name,
        first_name=student.first_name,
        middle_name=student.middle_name,
        birth_date=student.birth_date,
        email=student.email,
        phone_number=student.phone_number,
        address=student.address,
        gender=student.gender,
        budget_contract=student.budget_contract,
        status=student.status,
        group_id=student.group_id,
        education_level=student.education_level
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_student(db: Session, student_id: int, student_update: Dict[str, Any]):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        return None
    for key, value in student_update.items():
        setattr(db_student, key, value)
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        return False
    db.delete(db_student)
    db.commit()
    return True
