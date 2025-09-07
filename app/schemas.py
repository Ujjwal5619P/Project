from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ReportBase(BaseModel):
    hazard_type: str
    location: str
    description: str
    severity: str

class ReportCreate(ReportBase):
    is_official: Optional[bool] = False

class Report(ReportBase):
    id: int
    is_official: bool
    status: str
    created_at: datetime
    files: List[str] = []

    class Config:
        orm_mode = True
