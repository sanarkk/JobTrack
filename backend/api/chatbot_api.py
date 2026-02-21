from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.database.session import get_db
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
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    history = ""

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    headers = {
        "x-goog-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    prompt = f"""
    You are an ATS resume assistant.
    Provide short, but useful answers.

    Here are resume information in JSON:

    Task: {text}
    """

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    r = requests.post(url, headers=headers, json=payload)
    data = r.json()

    reply = data["candidates"][0]["content"]["parts"][0]["text"]
    return reply