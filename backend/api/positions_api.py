from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.database.session import get_db
from backend.models.position_model import Position


router = APIRouter()


@router.get("/all")
async def get_all_positions(db: Session = Depends(get_db)):
    return db.query(Position).limit(5).all()