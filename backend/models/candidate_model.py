from sqlalchemy import ARRAY, Column, Text, text
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from sqlalchemy.sql import func

from backend.database.session import Base


class CandidateResume(Base):
    __tablename__ = "candidate_resumes"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    user_email = Column(Text, nullable=False)

    file_name = Column(Text, nullable=False)
    file_path = Column(Text, nullable=True)
    extension = Column(Text, nullable=True)

    profile_name = Column(Text, nullable=True)
    email = Column(Text, nullable=True)
    mobile_number = Column(Text, nullable=True)
    designation = Column(Text, nullable=True)
    total_experience = Column(Text, nullable=True)
    education = Column(Text, nullable=True)

    skills = Column(
        ARRAY(Text),
        nullable=False,
        server_default=text("'{}'::text[]"),
    )

    company_names = Column(
        ARRAY(Text),
        nullable=False,
        server_default=text("'{}'::text[]"),
    )

    ai_summary = Column(Text, nullable=True)

    ai_strengths = Column(
        ARRAY(Text),
        nullable=False,
        server_default=text("'{}'::text[]"),
    )

    experiences = Column(
        JSONB,
        nullable=False,
        server_default=text("'[]'::jsonb"),
    )

    resume_json = Column(JSONB, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    )