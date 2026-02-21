from sqlalchemy import ARRAY, Column, Float, String, Text, text
from sqlalchemy.dialects.postgresql import UUID

from backend.database.session import Base


class Position(Base):
    __tablename__ = "marker_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))

    job_title = Column(Text, nullable=True)
    job_category = Column(Text, nullable=True)

    seniority_level = Column(Text, nullable=True)
    requirements_summary = Column(Text, nullable=True)
    technical_tools = Column(ARRAY(Text), nullable=True)
    formatted_workplace_location = Column(Text, nullable=True)
    province = Column(Text, nullable=True)
    commitment = Column(Text, nullable=True)
    workplace_type = Column(Text, nullable=True)

    yearly_min_compensation = Column(Float, nullable=True)
    yearly_max_compensation = Column(Float, nullable=True)
    company_name = Column(Text, nullable=True)
    apply_url = Column(Text, nullable=True)
    source_file = Column(Text, nullable=True)
    hash = Column(Text, nullable=True)
