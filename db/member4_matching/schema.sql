CREATE TABLE Availability_Slots (
    slot_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    start_time DATETIME NOT NULL,
    is_booked BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);