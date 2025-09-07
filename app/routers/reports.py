from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import shutil
import os
from app import crud, database

router = APIRouter(prefix="/reports", tags=["Reports"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Citizen: upload report
@router.post("/upload")
async def upload_report(
    hazard_type: str = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    severity: str = Form(...),
    files: List[UploadFile] = File(None),
    db: Session = Depends(get_db)  # <-- fixed here
):
    saved_files = []
    if files:
        for f in files:
            file_path = os.path.join(UPLOAD_DIR, f.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(f.file, buffer)
            saved_files.append(f"/uploads/{f.filename}")

    new_report = crud.create_report(
        db=db,
        hazard_type=hazard_type,
        location=location,
        description=description,
        severity=severity,
        files=saved_files,
        status="pending",
        is_official=False
    )
    return {"id": new_report.id}

# Admin: get all reports
@router.get("/admin")
def get_all_reports(db: Session = Depends(get_db)):  # <-- fixed here
    reports = crud.get_all_reports(db)
    return reports

# Citizen: get approved reports
@router.get("/citizen")
def get_citizen_reports(db: Session = Depends(get_db)):  # <-- fixed here
    reports = crud.get_approved_reports(db)
    return reports

# Admin: approve or reject report
@router.put("/admin/{report_id}/{action}")
def update_report_status(
    report_id: int,
    action: str,
    db: Session = Depends(get_db)  # <-- fixed here
):
    if action not in ["approve", "reject"]:
        raise HTTPException(status_code=400, detail="Invalid action")
    report = crud.get_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    new_status = "approved" if action == "approve" else "rejected"
    crud.update_report_status(db, report_id, new_status)
    return {"message": f"Report {report_id} {new_status}"}
# Admin: get official reports (already approved)
@router.get("/official")
def get_official_reports(db: Session = Depends(get_db)):
    reports = crud.get_official_reports(db)
    return reports

