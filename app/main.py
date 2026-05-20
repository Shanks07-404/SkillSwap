import os
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

app = FastAPI(title="SkillSwap Workspace Engine")

# -------------------------------------------------------------------------
# PYDANTIC VALIDATION SCHEMAS
# -------------------------------------------------------------------------
class SwapAllocationRequest(BaseModel):
    target_user_id: int
    hours_allocated: int


# -------------------------------------------------------------------------
# CORE BACKEND SEARCH ROUTE
# -------------------------------------------------------------------------
@app.get("/api/matching/search")
def run_discovery_matrix(skill: str, db: Session = Depends(get_db)):
    query = text("""
        SELECT 
            u.user_id AS expert_id,
            u.username AS user_name,      
            u.reputation_score,
            s.skill_name,
            us.role_type AS level, 
            'Flexible' AS availability    
        FROM Users u
        INNER JOIN User_Skills us ON u.user_id = us.user_id
        INNER JOIN Skills s ON us.skill_id = s.skill_id
        WHERE s.skill_name LIKE :sq
    """)
    
    try:
        results = db.execute(query, {"sq": f"%{skill}%"}).fetchall()
        return [dict(row._mapping) for row in results]
    except Exception as e:
        # THIS WILL PRINT THE EXACT VISUAL LOG DIRECTLY IN YOUR VS CODE TERMINAL
        print("\n=== !!! SEARCH ENDPOINT CRASH LOG !!! ===")
        print(str(e))
        print("=========================================\n")
        
        return JSONResponse(
            status_code=500, 
            content={"error": "Database Execution Failure", "details": str(e)}
        )


# -------------------------------------------------------------------------
# TRANSACTION & BALANCE ALLOCATION ENDPOINT
# -------------------------------------------------------------------------
@app.post("/api/transaction/allocate")
def process_swap_escrow_allocation(payload: SwapAllocationRequest, db: Session = Depends(get_db)):
    current_user_id = 2 
    
    try:
        log_trade_record = text("""
            INSERT INTO Trade_Logs (learner_id, expert_id, hours_exchanged, status)
            VALUES (:learner_id, :expert_id, :hours_exchanged, 'Pending')
        """)
        
        db.execute(log_trade_record, {
            "learner_id": current_user_id, 
            "expert_id": payload.target_user_id, 
            "hours_exchanged": payload.hours_allocated
        })
        
        db.commit() 
        return {"status": "Success", "detail": "Ledger logged! Match records successfully saved to Trade_Logs table."}
        
    except Exception as e:
        db.rollback()
        print("\n=== !!! ALLOCATION ENDPOINT CRASH LOG !!! ===")
        print(str(e))
        print("=============================================\n")
        
        return JSONResponse(
            status_code=500, 
            content={
                "status": "Failed Database Write", 
                "detail": f"Database exception raised: {str(e)}"
            }
        )


# --- Keep your other test routers active if needed ---
@app.post("/api/transaction/force-complete")
def force_transaction_complete_stub():
    return {"status": "Success", "detail": "Ledger state synchronized."}


# -------------------------------------------------------------------------
# STATIC UI & HOMEPAGE ASSET MANAGEMENT
# -------------------------------------------------------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_homepage():
    return FileResponse("static/index.html")