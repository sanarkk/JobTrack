from sqlalchemy import Column, Text, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from backend.database.session import Base


class ResumeJobMatch(Base):
    __tablename__ = "resume_job_match"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    job_id = Column(Text, nullable=False)
    user_gmail = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
