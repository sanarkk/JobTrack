from pathlib import Path

import requests
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.config import ENABLE_MATCHED_POSITIONS
from backend.database.session import get_db
from backend.dependencies.user_dependencies import get_email_from_token
from backend.models.candidate_model import CandidateResume
from backend.models.position_model import Position
from backend.models.saved_position_model import SavedJob
from backend.schemas.position_schema import MatchedPositionSchema, PositionSchema
from backend.services.matching_service import MatchingModelUnavailableError, compute_match_score


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BASE_DIR / "data" / "resume_in"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_MATCH_CANDIDATES = 500

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/all", response_model=list[PositionSchema])
async def get_all_positions(db: Session = Depends(get_db)):
    return db.query(Position).limit(10).all()


@router.get("/positions/matched", response_model=list[MatchedPositionSchema])
def get_matched_positions(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    min_score: float = Query(default=0.0, ge=0.0, le=100.0),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    if not ENABLE_MATCHED_POSITIONS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matched positions is disabled.")

    user_email = get_email_from_token(token)
    resume = (
        db.query(CandidateResume)
        .filter(CandidateResume.user_email == user_email)
        .order_by(CandidateResume.updated_at.desc())
        .first()
    )
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate resume not found.")

    jobs = (
        db.query(Position)
        .filter(Position.technical_tools.isnot(None))
        .filter(func.cardinality(Position.technical_tools) > 0)
        .limit(MAX_MATCH_CANDIDATES)
        .all()
    )

    resume_skills = resume.skills or []
    resume_title = resume.designation or resume.profile_name or ""

    scored_jobs: list[tuple[Position, float]] = []
    try:
        for job in jobs:
            score = compute_match_score(
                resume_skills=resume_skills,
                job_skills=job.technical_tools or [],
                resume_title=resume_title,
                job_title=job.job_title or "",
            )
            if score >= min_score:
                scored_jobs.append((job, score))
    except MatchingModelUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "code": "MATCHING_MODEL_UNAVAILABLE",
                "message": "Job matching model is unavailable.",
            },
        ) from exc

    scored_jobs.sort(key=lambda row: row[1], reverse=True)
    paged_jobs = scored_jobs[offset : offset + limit]

    response: list[MatchedPositionSchema] = []
    for job, score in paged_jobs:
        if hasattr(PositionSchema, "model_validate"):
            payload = PositionSchema.model_validate(job).model_dump()
        else:  # pragma: no cover - pydantic v1 compatibility path
            payload = PositionSchema.from_orm(job).dict()
        payload["matching_score"] = score
        response.append(MatchedPositionSchema(**payload))
    return response


@router.post("/upload_resume")
async def upload_resume(token: str = Depends(oauth2_scheme), file: UploadFile = File(...)):
    user_email = get_email_from_token(token)
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file.file.seek(0)
    files = {"file": (file.filename, file.file, file.content_type)}
    data = {"user_email": user_email}
    response = requests.post(
        "http://host.docker.internal:8002/parse_resume/resume/",
        files=files,
        data=data,
    )

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
            detail="Saved job not found",
        )

    return {
        "id": str(saved_job.id),
        "user_email": saved_job.user_email,
        "job_id": saved_job.job_id,
    }


@router.get("/get_all_saved_jobs")
def get_all_saved_jobs(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    user_email = get_email_from_token(token)
    saved_jobs = db.query(SavedJob).filter(SavedJob.user_email == user_email).all()

    result = [
        {
            "id": str(job.id),
            "user_email": job.user_email,
            "job_id": job.job_id,
        }
        for job in saved_jobs
    ]

    return result


@router.delete("/delete/{position_id}")
def delete_saved_job(
    position_id: str,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
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
            detail="Saved job not found",
        )

    db.delete(saved_job)
    db.commit()

    return {"message": "Saved job deleted successfully", "id": str(saved_job.id)}
