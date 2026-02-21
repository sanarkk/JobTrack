from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class PositionSchema(BaseModel):
    id: str
    search_term: Optional[str]
    salary_min: Optional[str]
    salary_max: Optional[str]
    salary_mid: Optional[str]
    core_job_title: Optional[str]
    location: Optional[str]
    date_posted: Optional[datetime]
    description: Optional[str]
    job_category: Optional[str]
    seniority_level: Optional[str]
    technical_tools: Optional[Any]
    workplace_type: Optional[str]
    company_industry: Optional[Any]
    company_size: Optional[str]
    company_sector_and_industry: Optional[str]
    min_industry_and_role_yoe: Optional[str]
    listed_compensation_currency: Optional[str]

    class Config:
        orm_mode = True