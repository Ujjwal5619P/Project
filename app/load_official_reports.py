# load_official_reports.py

import json
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud

FILE_PATH = "app/official_reports.json"

def load_official_reports():
    db: Session = SessionLocal()
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            reports = json.load(f)

        for report in reports:
            # Force official + approved before saving
            report["status"] = "approved"
            report["is_official"] = True
            crud.create_official_report(db, report)

        print(f"✅ Loaded {len(reports)} official reports into DB")
    finally:
        db.close()

if __name__ == "__main__":
    load_official_reports()
