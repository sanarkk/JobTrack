from sqlalchemy import Column, Float, Text, DateTime, text
from sqlalchemy.dialects.postgresql import UUID

from backend.database.session import Base


class ResumeJobMatch(Base):
    __tablename__ = "resume_job_match"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    job_id = Column(Text, nullable=False)
    user_gmail = Column(Text, nullable=False)

    matching_rate = Column(Float, nullable=True)

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("now()")
    )