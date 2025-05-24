from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date
from ..models.models import Faculty, Program, Group, Student


class FacultyBase(BaseModel):
    name: str


class FacultyCreate(FacultyBase):
    pass


class Faculty(FacultyBase):
    id: int
    programs: List['Program'] = []

    class Config:
        from_attributes = True


class ProgramBase(BaseModel):
    name: str
    faculty_id: int
    education_level: str


class ProgramCreate(ProgramBase):
    pass


class Program(ProgramBase):
    id: int
    faculty: Optional['Faculty'] = None
    groups: List['Group'] = []

    class Config:
        from_attributes = True


class GroupBase(BaseModel):
    name: str
    program_id: int
    study_form: str
    education_level: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    program: Optional['Program'] = None
    students: List['Student'] = []

    class Config:
        from_attributes = True


class StudentBase(BaseModel):
    last_name: str
    first_name: str
    middle_name: str
    birth_date: Optional[date] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    gender: Optional[str] = None
    budget_contract: str
    status: str
    group_id: int
    education_level: str


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int
    group: Optional['Group'] = None

    class Config:
        from_attributes = True


# Для разрешения циклических зависимостей
Faculty.update_forward_refs(Program=Program)
Program.update_forward_refs(Group=Group)
Group.update_forward_refs(Student=Student)