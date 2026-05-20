from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter(prefix="/identity", tags=["Member 1: Identity & Profile"])

@router.get("/profile/{user_id}")
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    query = text("SELECT user_id, username, reputation_score FROM Users WHERE user_id = :uid")
    result = db.execute(query, {"uid": user_id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="User Identity not found.")
    return dict(result._mapping)