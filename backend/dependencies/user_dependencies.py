from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.models.user_model import User
from typing import Optional
from backend.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import uuid
from jose import jwt, JWTError


def get_email_from_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        data: str = payload.get("sub")
        if data is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return data
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data: dict) -> User:
    if "id" not in user_data:
        user_data["id"] = str(uuid.uuid4())

    user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=user_data["password"],
        )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
