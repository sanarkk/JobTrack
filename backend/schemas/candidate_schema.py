from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List, Dict, Any


class CandidateResumeSchema(BaseModel):
    id: Optional[str | UUID]
    user_id: Optional[str | UUID]

    file_name: str
    file_path: Optional[str]
    extension: Optional[str]

    profile_name: Optional[str]
    email: Optional[str]
    mobile_number: Optional[str]
    designation: Optional[str]
    total_experience: Optional[str]
    education: Optional[str]

    skills: Optional[List[str]]
    company_names: Optional[List[str]]

    ai_summary: Optional[str]
    ai_strengths: Optional[List[str]]

    experiences: Optional[List[Dict[str, Any]]]

    resume_json: Dict[str, Any]

    class Config:
        orm_mode = True