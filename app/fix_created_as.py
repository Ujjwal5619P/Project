# fix_created_at.py
from datetime import datetime
from app.database import SessionLocal
from app.models import Report

def fix_created_at():
    db = SessionLocal()
    try:
        # Find rows with NULL created_at
        reports = db.query(Report).filter(Report.created_at == None).all()
        print(f"Found {len(reports)} rows with NULL created_at.")

        if reports:
            for r in reports:
                r.created_at = datetime.utcnow()
            db.commit()
            print("Updated all NULL created_at rows.")
        else:
            print("No NULL created_at rows found. Nothing to update.")

    except Exception as e:
        print("Error:", e)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_created_at()
