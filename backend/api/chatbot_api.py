from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.database.session import get_db
from backend.models.candidate_model import CandidateResume
from backend.dependencies.user_dependencies import get_email_from_token
import requests
from backend.config import GEMINI_API_KEY as API_KEY
import json
from fastapi import HTTPException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

@router.post("/chatbot/send_message_ai/")
async def start_chat(
    text: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    user_email = get_email_from_token(token)

    resume = db.query(CandidateResume).filter(CandidateResume.user_email == user_email).first()

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
    }

    print(resume_data)

    resume_json_str = json.dumps(resume_data, indent=2)

    prompt = f"""
    You are an ATS resume assistant.
    Provide short, but useful answers.

    Here is the user's resume information in JSON:
    {resume_json_str}

    Task: {text}
    """

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {
        "x-goog-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }

    r = requests.post(url, headers=headers, json=payload)
    data = r.json()

    reply = data["candidates"][0]["content"]["parts"][0]["text"]
    return {"reply": reply}