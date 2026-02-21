from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pathlib import Path
from fastapi.security import OAuth2PasswordBearer
import uuid
from sqlalchemy.dialects.postgresql import UUID
import shutil
from backend.dependencies.user_dependencies import get_email_from_token
import requests
from sqlalchemy.orm import Session
from backend.schemas.position_schema import PositionSchema
from sqlalchemy import text, cast
from backend.database.session import get_db
from backend.models.saved_position_model import SavedJob
from backend.models.position_model import Position


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BASE_DIR / "data" / "resume_in"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {".pdf", ".docx"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



@router.get("/all", response_model=list[PositionSchema])
async def get_all_positions(db: Session = Depends(get_db)):
    return db.query(Position).limit(10).all()


@router.post("/upload_resume")
async def upload_resume(token: str = Depends(oauth2_scheme), file: UploadFile = File(...)):
    user_email = get_email_from_token(token)
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file.file.seek(0)
    files = {"file": (file.filename, file.file, file.content_type)}
    data = {
        "user_email": user_email
    }
    response = requests.post("http://host.docker.internal:8002/parse_resume/resume/", files=files, data=data)

    return response.json()


@router.post("/save_position")
async def save_position(position_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_email = get_email_from_token(token)
    new_saved_job = SavedJob(user_email=user_email, job_id=position_id)
    db.add(new_saved_job)
    db.commit()
    db.refresh(new_saved_job)
    return {"message": "Position saved successfully", "id": str(new_saved_job.id)}


@router.get("/get_one/{position_id}")
async def get_one_position(position_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_email = get_email_from_token(token)

    saved_job = (
        db.query(SavedJob)
        .filter(SavedJob.job_id == position_id, SavedJob.user_email == user_email)
        .first()
    )

    if not saved_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved job not found"
        )

    return {
        "id": str(saved_job.id),
        "user_email": saved_job.user_email,
        "job_id": saved_job.job_id
    }

@router.get("/get_all_saved_jobs")
def get_all_saved_jobs(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_email = get_email_from_token(token)

    saved_jobs = (
        db.query(SavedJob, Position)
        .join(Position, cast(SavedJob.job_id, UUID) == Position.id)
        .filter(SavedJob.user_email == user_email)
        .all()
    )

    result = []
    for saved_job, position in saved_jobs:
        result.append({
            "saved_id": str(saved_job.id),
            "job_id": str(position.id),
            "job_title": position.job_title,
            "job_category": position.job_category,
            "seniority_level": position.seniority_level,
            "requirements_summary": position.requirements_summary,
            "technical_tools": position.technical_tools,
            "formatted_workplace_location": position.formatted_workplace_location,
            "province": position.province,
            "commitment": position.commitment,
            "workplace_type": position.workplace_type,
            "yearly_min_compensation": position.yearly_min_compensation,
            "yearly_max_compensation": position.yearly_max_compensation,
            "company_name": position.company_name,
            "apply_url": position.apply_url,
            "source_file": position.source_file,
            "hash": position.hash
        })

    return result


@router.delete("/delete/{position_id}")
def delete_saved_job(
    position_id: str,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_email = get_email_from_token(token)
    saved_job = (
        db.query(SavedJob)
        .filter(SavedJob.job_id == position_id, SavedJob.user_email == user_email)
        .first()
    )

    if not saved_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved job not found"
        )

    db.delete(saved_job)
    db.commit()

    return {"message": "Saved job deleted successfully", "id": str(saved_job.id)}