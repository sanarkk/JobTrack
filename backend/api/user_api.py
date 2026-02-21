from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from backend.auth.auth import get_password_hash, verify_password, create_access_token
from backend.dependencies.user_dependencies import get_user_by_email, create_user, get_email_from_token
from backend.database.session import get_db
from backend.models.candidate_model import CandidateResume
from sqlalchemy.orm import Session
from jose import jwt
import time
from backend.schemas.user_schemas import UserCreate, UserOut
from backend.config import METABASE_SECRET_KEY

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/")


@router.post("/register/", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = get_password_hash(user.password)
    user_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": hashed_password,
    }

    new_user = create_user(db, user_data)
    return new_user


@router.post("/token/")
def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = get_user_by_email(db, form_data.username)


    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/me/")
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    data = get_email_from_token(token=token)
    user = get_user_by_email(db, data)

    return user


@router.get("/my_resume/")
async def get_resume(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = get_email_from_token(token)

    resume = db.query(CandidateResume).filter(CandidateResume.user_email == email).first()

    if not resume:
        return {"error": "Resume not found for this user."}

    resume_data = {
        "profile_name": resume.profile_name,
        "user_email": resume.user_email,
        "mobile_number": resume.mobile_number,
        "designation": resume.designation,
        "total_experience": resume.total_experience,
        "education": resume.education,
        "skills": resume.skills,
        "company_names": resume.company_names,
        "ai_summary": resume.ai_summary,
        "ai_strengths": resume.ai_strengths,
        "experiences": resume.experiences,
        "resume_json": resume.resume_json
    }

    return resume_data


@router.post("/generate_metabase_token/")
async def generate_metabase_token():
    payload = {
        "resource": {"dashboard": 3},
        "params": {},
        "exp": int(time.time()) + (10 * 60)  # 10 minutes
    }

    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

    return {"token": token}