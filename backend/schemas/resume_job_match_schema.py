from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ResumeJobMatchSchema(BaseModel):
    id: Optional[str | UUID]
    job_id: str
    user_gmail: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
