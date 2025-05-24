from sqlalchemy import Column, Integer, String, Date, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from ..database import Base


class Faculty(Base):
    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    programs = relationship("Program", back_populates="faculty")


class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculties.id"))
    education_level = Column(String(20), nullable=False)

    faculty = relationship("Faculty", back_populates="programs")
    groups = relationship("Group", back_populates="program")


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id"))
    study_form = Column(String(20), nullable=False)
    education_level = Column(String(20), nullable=False)

    program = relationship("Program", back_populates="groups")
    students = relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=False)
    birth_date = Column(Date)
    email = Column(String(100))
    phone_number = Column(String(15))
    address = Column(String(255))
    gender = Column(CHAR(1))
    budget_contract = Column(String(20), nullable=False)
    status = Column(String(50), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))
    education_level = Column(String(20), nullable=False)

    group = relationship("Group", back_populates="students")


