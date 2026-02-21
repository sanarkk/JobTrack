from pydantic import BaseModel
from typing import Optional, List

class PositionSchema(BaseModel):
    id: Optional[str]
    job_title: Optional[str]
    job_category: Optional[str]
    seniority_level: Optional[str]
    requirements_summary: Optional[str]
    technical_tools: Optional[List[str]]
    formatted_workplace_location: Optional[str]
    province: Optional[str]
    commitment: Optional[str]
    workplace_type: Optional[str]
    yearly_min_compensation: Optional[float]
    yearly_max_compensation: Optional[float]
    company_name: Optional[str]
    apply_url: Optional[str]
    source_file: Optional[str]
    hash: Optional[str]

    class Config:
        orm_mode = True
