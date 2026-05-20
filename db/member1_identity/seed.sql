-- Disable safe updates and constraint checks to clear records cleanly
SET SQL_SAFE_UPDATES = 0;
SET FOREIGN_KEY_CHECKS = 0;

-- Wipe tables completely (Order doesn't matter while checks are 0)
DELETE FROM Trade_Logs;
DELETE FROM User_Skills;
DELETE FROM Skills;
DELETE FROM Users;

-- Restore standard database protective safety checks
SET FOREIGN_KEY_CHECKS = 1;
SET SQL_SAFE_UPDATES = 1;

-- 1. Populating our dynamic system member array with varied rankings
INSERT INTO Users (user_id, username, reputation_score) VALUES 
(1, 'AliceDev', 5.00),     -- Expert Node
(2, 'BobMusic', 4.80),     -- Expert Node
(3, 'CharlieChef', 4.90),  -- Expert Node
(4, 'DanaData', 3.65),     -- Average / Intermediate Node
(5, 'EvanJava', 2.40),     -- Beginner Node
(6, 'FionaDesign', 1.80);  -- Beginner Node

-- 2. Registering clean skill configurations
INSERT INTO Skills (skill_id, skill_name) VALUES 
(1, 'Python Programming'),
(2, 'Guitar Lessons'),
(3, 'French Cooking'),
(4, 'UI/UX Mobile Design');

-- 3. Binding multi-tier capabilities via dynamic role_types
INSERT INTO User_Skills (user_id, skill_id, role_type) VALUES 
(1, 1, 'Expert'),          -- Alice is a Python Expert
(1, 2, 'Learner'),      
(2, 2, 'Expert'),          -- Bob is a Guitar Expert
(2, 1, 'Learner'),      
(3, 3, 'Expert'),          -- Charlie is a Cooking Expert
(4, 1, 'Intermediate'),    -- Dana is an Average/Intermediate Python user
(5, 1, 'Beginner'),        -- Evan is a Python Beginner
(6, 4, 'Intermediate'),    -- Fiona is an Intermediate Designer
(6, 1, 'Beginner');        -- Fiona is a Beginner at Python