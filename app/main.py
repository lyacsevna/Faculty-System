from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from io import BytesIO
import openpyxl

from . import models
from .database import SessionLocal, engine
from .schemas import schemas
from .crud import crud

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все origins (для разработки)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Faculty endpoints
@app.post("/faculties/", response_model=schemas.Faculty, status_code=status.HTTP_201_CREATED)
def create_faculty(faculty: schemas.FacultyCreate, db: Session = Depends(get_db)):
    return crud.create_faculty(db=db, faculty=faculty)


@app.get("/faculties/", response_model=list[schemas.Faculty])
def read_faculties(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_faculties(db, skip=skip, limit=limit)


@app.put("/faculties/{faculty_id}", response_model=schemas.Faculty)
def update_faculty(faculty_id: int, faculty: schemas.FacultyUpdate, db: Session = Depends(get_db)):
    updated_faculty = crud.update_faculty(db=db, faculty_id=faculty_id, faculty=faculty)
    if not updated_faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return updated_faculty


@app.delete("/faculties/{faculty_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faculty(faculty_id: int, db: Session = Depends(get_db)):
    if not crud.delete_faculty(db=db, faculty_id=faculty_id):
        raise HTTPException(status_code=404, detail="Faculty not found")


# Program endpoints
@app.post("/programs/", response_model=schemas.Program, status_code=status.HTTP_201_CREATED)
def create_program(program: schemas.ProgramCreate, db: Session = Depends(get_db)):
    return crud.create_program(db=db, program=program)


@app.get("/programs/", response_model=list[schemas.Program])
def read_programs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_programs(db, skip=skip, limit=limit)


@app.put("/programs/{program_id}", response_model=schemas.Program)
def update_program(program_id: int, program: schemas.ProgramUpdate, db: Session = Depends(get_db)):
    updated_program = crud.update_program(db=db, program_id=program_id, program=program)
    if not updated_program:
        raise HTTPException(status_code=404, detail="Program not found")
    return updated_program


@app.delete("/programs/{program_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_program(program_id: int, db: Session = Depends(get_db)):
    if not crud.delete_program(db=db, program_id=program_id):
        raise HTTPException(status_code=404, detail="Program not found")


# Group endpoints
@app.post("/groups/", response_model=schemas.Group, status_code=status.HTTP_201_CREATED)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    return crud.create_group(db=db, group=group)


@app.get("/groups/", response_model=list[schemas.Group])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_groups(db, skip=skip, limit=limit)


@app.put("/groups/{group_id}", response_model=schemas.Group)
def update_group(group_id: int, group: schemas.GroupUpdate, db: Session = Depends(get_db)):
    updated_group = crud.update_group(db=db, group_id=group_id, group=group)
    if not updated_group:
        raise HTTPException(status_code=404, detail="Group not found")
    return updated_group


@app.delete("/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    if not crud.delete_group(db=db, group_id=group_id):
        raise HTTPException(status_code=404, detail="Group not found")


# Student endpoints
@app.post("/students/", response_model=schemas.Student, status_code=status.HTTP_201_CREATED)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db=db, student=student)


@app.get("/students/", response_model=list[schemas.Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_students(db, skip=skip, limit=limit)


@app.put("/students/{student_id}", response_model=schemas.Student)
def update_student(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    updated_student = crud.update_student(db=db, student_id=student_id, student=student)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    if not crud.delete_student(db=db, student_id=student_id):
        raise HTTPException(status_code=404, detail="Student not found")


# Excel Export/Import endpoints
@app.get("/export/excel/")
def export_data_to_excel(
        entity_type: str = Query(..., description="Type of entity to export (faculty, program, group, student)"),
        include_ids: bool = Query(True, description="Include IDs in export"),
        db: Session = Depends(get_db)
):
    try:
        excel_buffer = crud.export_entities_to_excel(db, entity_type, include_ids)
        return StreamingResponse(
            excel_buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={entity_type}_export.xlsx"}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/import/excel/", response_model=schemas.ExcelImportResponse)
async def import_data_from_excel(
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls) are supported")

    try:
        result = crud.import_entities_from_excel(db, file)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Additional endpoints
@app.get("/faculties/{faculty_id}/programs", response_model=list[schemas.Program])
def read_faculty_programs(faculty_id: int, db: Session = Depends(get_db)):
    programs = crud.get_faculty_programs(db, faculty_id=faculty_id)
    if not programs:
        raise HTTPException(status_code=404, detail="No programs found for this faculty")
    return programs


@app.get("/programs/{program_id}/groups", response_model=list[schemas.Group])
def read_program_groups(program_id: int, db: Session = Depends(get_db)):
    groups = crud.get_program_groups(db, program_id=program_id)
    if not groups:
        raise HTTPException(status_code=404, detail="No groups found for this program")
    return groups


@app.get("/groups/{group_id}/students", response_model=list[schemas.Student])
def read_group_students(
        group_id: int,
        budget_contract: Optional[str] = None,
        status: Optional[str] = None,
        gender: Optional[str] = None,
        db: Session = Depends(get_db)
):
    students = crud.get_group_students(
        db,
        group_id=group_id,
        budget_contract=budget_contract,
        status=status,
        gender=gender
    )
    if not students:
        raise HTTPException(status_code=404, detail="No students found for this group")
    return students