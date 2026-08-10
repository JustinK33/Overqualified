-- use this when we need to create table or wtv change names and stuff according to what u need
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY
    username VARCHAR(50) NOT NULL
    hashed_password BYTEA NOT NULL
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)