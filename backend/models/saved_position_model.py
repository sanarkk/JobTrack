from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from backend.database.session import Base

class SavedJob(Base):
    __tablename__ = "saved_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_email = Column(String(50), nullable=False, index=True)
    job_id = Column(String(50), nullable=False)