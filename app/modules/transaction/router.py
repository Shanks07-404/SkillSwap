import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter(prefix="/transactions", tags=["Member 3: Atomic Engine"])

@router.post("/request")
def process_atomic_trade(learner_id: int, expert_id: int, hours: int, slot_id: int, db: Session = Depends(get_db)):
    # Start clean context manager block for true explicit atomicity rollbacks
    with db.begin():
        try:
            # Step A: Lock balance via Member 2's explicit stored procedure
            db.execute(text("CALL sp_lock_balance(:uid, :h)"), {"uid": learner_id, "h": hours})
            
            # Step B: 5-Second Processing Delay Requirement
            time.sleep(5)
            
            # Step C: Log transaction inside Member 3's infrastructure
            db.execute(
                text("""
                    INSERT INTO Trade_Logs (learner_id, expert_id, hours_exchanged, status) 
                    VALUES (:l, :e, :h, 'Pending')
                """),
                {"l": learner_id, "e": expert_id, "h": hours}
            )
            
            # Step D: Block out the calendar schedule space inside Member 4's domain
            db.execute(
                text("UPDATE Availability_Slots SET is_booked = TRUE WHERE slot_id = :sid"),
                {"sid": slot_id}
            )
            
            return {"status": "success", "message": "Transaction committed and logged successfully."}

        except Exception as e:
            # Automatically rolls back the implicit transaction context block
            raise HTTPException(status_code=400, detail=f"Atomic Isolation Aborted: {str(e)}")

@router.post("/complete/{trade_id}")
def verify_and_complete_trade(trade_id: int, db: Session = Depends(get_db)):
    with db.begin():
        # Grab target log metadata first
        find_query = text("SELECT learner_id, expert_id, hours_exchanged, status FROM Trade_Logs WHERE trade_id = :tid")
        trade = db.execute(find_query, {"tid": trade_id}).fetchone()
        
        if not trade or trade._mapping['status'] != 'Pending':
            raise HTTPException(status_code=400, detail="Trade record missing or already finalized.")
        
        t_data = trade._mapping
        
        # Release the locked hours and move to expert's balance
        db.execute(
            text("""
                UPDATE Vault_Balances 
                SET locked_hours = locked_hours - :h 
                WHERE user_id = :lid
            """), {"h": t_data['hours_exchanged'], "lid": t_data['learner_id']}
        )
        
        db.execute(
            text("""
                UPDATE Vault_Balances 
                SET available_hours = available_hours + :h 
                WHERE user_id = :eid
            """), {"h": t_data['hours_exchanged'], "eid": t_data['expert_id']}
        )
        
        # Change status string to fire off the reputation recalculation trigger
        db.execute(text("UPDATE Trade_Logs SET status = 'Completed' WHERE trade_id = :tid"), {"tid": trade_id})
        
        return {"status": "success", "message": "Balances released and reputation score incremented."}