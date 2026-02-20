from sqlalchemy import Column, String, DateTime, Float, BigInteger, Numeric, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from backend.database.session import Base

class Position(Base):
    __tablename__ = "market_jobs"
    id = Column(String(200), primary_key=True)
    search_term = Column(String(150), nullable=False)
    salary_min = Column(String, nullable=False)
    salary_max = Column(String, nullable=False)
    salary_mid = Column(String, nullable=False)
    core_job_title = Column(String(150), nullable=False)
    location = Column(String(150), nullable=False)
    date_posted = Column(DateTime, default=func.now(), nullable=False)
    description = Column(Text, nullable=False)
    job_category = Column(String(150), nullable=False)
    seniority_level = Column(String(150), nullable=False)
    technical_tools = Column(JSON, nullable=False)
    workplace_type = Column(String(150), nullable=False)
    company_industry = Column(JSON, nullable=False)
    company_size = Column(String, nullable=False)
    company_sector_and_industry = Column(String(150), nullable=False)
    min_industry_and_role_yoe = Column(String(150), nullable=True)
    listed_compensation_currency = Column(String(150), nullable=False)