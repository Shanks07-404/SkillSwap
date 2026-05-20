
CREATE TABLE Vault_Balances (
    user_id INT PRIMARY KEY,
    available_hours INT DEFAULT 10,
    locked_hours INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- STORED PROCEDURE FOR BALANCE LOCKING
DELIMITER $$

CREATE PROCEDURE sp_lock_balance(IN p_user_id INT, IN p_hours INT)
BEGIN
    DECLARE current_balance INT;
    SELECT available_hours INTO current_balance 
    FROM Vault_Balances 
    WHERE user_id = p_user_id;
    
    IF current_balance >= p_hours THEN
        UPDATE Vault_Balances 
        SET available_hours = available_hours - p_hours, 
            locked_hours = locked_hours + p_hours
        WHERE user_id = p_user_id;
    ELSE
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Insufficient available hours to process this trade request.';
    END IF;
END$$

DELIMITER ;

select * from Vault_Balances;
