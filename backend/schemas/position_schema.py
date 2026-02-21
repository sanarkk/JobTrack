from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List

try:
    from pydantic import ConfigDict  # pydantic v2
except ImportError:  # pragma: no cover - pydantic v1 compatibility
    ConfigDict = None


class PositionSchema(BaseModel):
    id: Optional[str|UUID]
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

    if ConfigDict is not None:
        model_config = ConfigDict(from_attributes=True)
    else:  # pragma: no cover - pydantic v1 compatibility
        class Config:
            orm_mode = True


class MatchedPositionSchema(PositionSchema):
    matching_score: float
