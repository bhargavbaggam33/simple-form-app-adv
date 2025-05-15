-- Create the database
CREATE DATABASE IF NOT EXISTS form_app;

-- Use the database
USE form_app;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
);

-- Create user with secrets
CREATE USER IF NOT EXISTS 'app_user'@'%' IDENTIFIED BY 'user@123';
GRANT ALL PRIVILEGES ON form_app.* TO 'app_user'@'%';
FLUSH PRIVILEGES;

