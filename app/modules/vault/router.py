from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter(prefix="/vault", tags=["Member 2: Ledger Vault"])

@router.get("/balance/{user_id}")
def check_ledger_balance(user_id: int, db: Session = Depends(get_db)):
    query = text("SELECT user_id, available_hours, locked_hours FROM Vault_Balances WHERE user_id = :uid")
    result = db.execute(query, {"uid": user_id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="No ledger profile assigned to user.")
    return dict(result._mapping)