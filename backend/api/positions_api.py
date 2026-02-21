from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pathlib import Path
from fastapi.security import OAuth2PasswordBearer
import uuid
import shutil
from backend.dependencies.user_dependencies import get_email_from_token
import requests
from sqlalchemy.orm import Session
from backend.schemas.position_schema import PositionSchema
from sqlalchemy import text
from backend.database.session import get_db
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
