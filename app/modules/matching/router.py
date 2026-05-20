from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter(prefix="/matching", tags=["Member 4: Complex Matrix Discovery"])

@router.get("/search")
def run_discovery_matrix(skill: str, db: Session = Depends(get_db)):
    # Loosened up relational JOIN sequence for optimal presentation demo delivery
    query = text("""
        SELECT 
            u.user_id AS expert_id,
            u.username AS user_name,      -- Aligns perfectly with match.user_name in script.js
            u.reputation_score,
            s.skill_name,
            us.proficiency_level AS level, -- Aligns perfectly with match.level in script.js
            'Flexible' AS availability    -- Fallback static value matching UI script expectations
        FROM Users u
        INNER JOIN User_Skills us ON u.user_id = us.user_id
        INNER JOIN Skills s ON us.skill_id = s.skill_id
        WHERE s.skill_name LIKE :sq
    """)
    
    # Executes the query using the exact argument passed from the frontend URL parameters
    results = db.execute(query, {"sq": f"%{skill}%"}).fetchall()
    return [dict(row._mapping) for row in results]