from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.types import JSON
from datetime import datetime
from .database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    hazard_type = Column(String, nullable=False)
    location = Column(String, nullable=False)
    description = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, approved, rejected
    is_official = Column(Boolean, default=False)
    files = Column(JSON, default=[])  # list of file paths
    created_at = Column(DateTime, default=datetime.utcnow)
