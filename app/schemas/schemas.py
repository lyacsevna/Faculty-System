from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date
from enum import Enum


# Enums для валидации
class EducationLevel(str, Enum):
    BACHELOR = "бакалавриат"
    SPECIALIST = "специалитет"
    MASTER = "магистратура"
    SPO = "спо"
    POSTGRADUATE = "аспирантура"
    RESIDENCY = "ординатура"


class StudyForm(str, Enum):
    FULL_TIME = "очно"
    PART_TIME = "заочно"
    MIXED = "очно-заочно"


class BudgetContract(str, Enum):
    BUDGET = "бюджет"
    CONTRACT = "контракт"


class StudentStatus(str, Enum):
    STUDYING = "учится"
    ACADEMIC_LEAVE = "академический отпуск"
    EXPELLED = "отчислен"
    REINSTATED = "восстановился"


class Gender(str, Enum):
    MALE = "М"
    FEMALE = "Ж"


# Faculty Schemas
class FacultyBase(BaseModel):
    name: str = Field(..., max_length=100, example="Информационные технологии")


class FacultyCreate(FacultyBase):
    pass


class FacultyUpdate(FacultyBase):
    pass


class Faculty(FacultyBase):
    id: int

    class Config:
        from_attributes = True


# Program Schemas
class ProgramBase(BaseModel):
    name: str = Field(..., max_length=100, example="Программная инженерия")
    faculty_id: int = Field(..., gt=0, example=1)
    education_level: EducationLevel


class ProgramCreate(ProgramBase):
    pass


class ProgramUpdate(ProgramBase):
    pass


class Program(ProgramBase):
    id: int

    class Config:
        from_attributes = True


# Group Schemas
class GroupBase(BaseModel):
    name: str = Field(..., max_length=50, example="ПИ-21-1")
    program_id: int = Field(..., gt=0, example=1)
    study_form: StudyForm
    education_level: EducationLevel


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    pass


class Group(GroupBase):
    id: int

    class Config:
        from_attributes = True


# Student Schemas
class StudentBase(BaseModel):
    last_name: str = Field(..., max_length=50, example="Иванов")
    first_name: str = Field(..., max_length=50, example="Иван")
    middle_name: str = Field(..., max_length=50, example="Иванович")
    birth_date: Optional[date] = Field(None, example="2000-01-01")
    email: Optional[EmailStr] = Field(None, example="student@example.com")
    phone_number: Optional[str] = Field(None, max_length=15, example="+79991234567")
    address: Optional[str] = Field(None, max_length=255, example="ул. Примерная, 123")
    gender: Optional[Gender] = None
    budget_contract: BudgetContract
    status: StudentStatus
    group_id: int = Field(..., gt=0, example=1)
    education_level: EducationLevel


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True

class ExcelImportResponse(BaseModel):
    message: str
    total_records: int
    imported_records: int
    skipped_records: int
    errors: Optional[List[str]] = None

class ExportOptions(BaseModel):
    entity_type: str = Field(..., description="Type of entity to export (faculty, program, group, student)")
    include_ids: bool = Field(True, description="Include IDs in export")