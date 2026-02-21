from sqlalchemy import Column, String, DateTime, Float, BigInteger, Numeric, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from backend.database.session import Base

class Position(Base):
    __tablename__ = "market_jobs_test"
    id = Column(String(200), primary_key=True)
    search_term = Column(String(150), nullable=True)
    salary_min = Column(String, nullable=True)
    salary_max = Column(String, nullable=True)
    salary_mid = Column(String, nullable=True)
    core_job_title = Column(String(150), nullable=True)
    location = Column(String(150), nullable=True)
    date_posted = Column(DateTime, default=func.now(), nullable=True)
    description = Column(Text, nullable=True)
    job_category = Column(String(150), nullable=True)
    seniority_level = Column(String(150), nullable=True)
    technical_tools = Column(JSON, nullable=True)
    workplace_type = Column(String(150), nullable=True)
    company_industry = Column(JSON, nullable=True)
    company_size = Column(String, nullable=True)
    company_sector_and_industry = Column(String(150), nullable=True)
    min_industry_and_role_yoe = Column(String(150), nullable=True)
    listed_compensation_currency = Column(String(150), nullable=True)