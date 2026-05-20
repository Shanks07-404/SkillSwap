
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    reputation_score DECIMAL(3, 2) DEFAULT 5.00
);

CREATE TABLE Skills (
    skill_id INT AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE User_Skills (
    user_id INT,
    skill_id INT,
    role_type VARCHAR(20), -- 'Expert' or 'Learner'
    PRIMARY KEY (user_id, skill_id, role_type),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES Skills(skill_id) ON DELETE CASCADE
);

