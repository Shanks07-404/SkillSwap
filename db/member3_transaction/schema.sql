CREATE TABLE Trade_Logs (
    trade_id INT AUTO_INCREMENT PRIMARY KEY,
    learner_id INT,
    expert_id INT,
    hours_exchanged INT,
    status VARCHAR(20) DEFAULT 'Pending', -- 'Pending', 'Completed', 'Cancelled'
    FOREIGN KEY (learner_id) REFERENCES Users(user_id),
    FOREIGN KEY (expert_id) REFERENCES Users(user_id)
);

-- REPUTATION TRIGGER (Triggers updates on Member 1's tables)
DELIMITER $$

CREATE TRIGGER trg_trade_completion
AFTER UPDATE ON Trade_Logs
FOR EACH ROW
BEGIN
    IF NEW.status = 'Completed' AND OLD.status = 'Pending' THEN
        -- Reward Learner trust score
        UPDATE Users 
        SET reputation_score = LEAST(reputation_score + 0.1, 5.0) 
        WHERE user_id = NEW.learner_id;
        
        -- Reward Expert trust score
        UPDATE Users 
        SET reputation_score = LEAST(reputation_score + 0.1, 5.0) 
        WHERE user_id = NEW.expert_id;
    END IF;
END$$

DELIMITER ;

select * from Trade_Logs;
