from sqlalchemy.orm import Session
from . import models

def create_report(db: Session, hazard_type, location, description, severity, files, status, is_official):
    report = models.Report(
        hazard_type=hazard_type,
        location=location,
        description=description,
        severity=severity,
        files=files,
        status=status,
        is_official=is_official
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def get_all_reports(db: Session):
    return db.query(models.Report).all()

def get_approved_reports(db: Session):
    return db.query(models.Report).filter(models.Report.status == "approved").all()

def get_report(db: Session, report_id: int):
    return db.query(models.Report).filter(models.Report.id == report_id).first()

def update_report_status(db: Session, report_id: int, status: str):
    report = get_report(db, report_id)
    if report:
        report.status = status
        db.commit()
        db.refresh(report)
    return report
def get_official_reports(db: Session):
    return db.query(models.Report).filter(models.Report.is_official == True).all()

    
