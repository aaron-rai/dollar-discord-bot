-- name: add_user!
-- Add a new user to the users table
-- :param user_id: The Discord ID of the user to be added
-- :param user_name: The username of the user to be added
-- :param home_address: The home address of the user
-- :param work_address: The work address of the user
-- :param time_zone: The time zone of the user
INSERT INTO users (discord_id, username, home_address, work_address, time_zone)
VALUES (:user_id, :user_name, :home_address, :work_address, :time_zone);

-- name: check_user_exists^
-- Check if a user exists in the users table
-- :param user_name: The username of the user to check for existence
SELECT username FROM users WHERE username = :user_name;

-- name: update_users_home_address!
-- Update the home address of a user
-- :param user_name: The username of the user whose home address is to be updated
-- :param home_address: The new home address of the user
UPDATE users SET home_address = :home_address WHERE username = :user_name;

-- name: update_users_work_address!
-- Update the work address of a user
-- :param user_name: The username of the user whose work address is to be updated
-- :param work_address: The new work address of the user
UPDATE users SET work_address = :work_address WHERE username = :user_name;

-- name: update_users_time_zone!
-- Update the time zone of a user
-- :param user_name: The username of the user whose time zone is to be updated
-- :param time_zone: The new time zone of the user
UPDATE users SET time_zone = :time_zone WHERE username = :user_name;

-- name: get_users_home_address^
-- Get the home address of a user
-- :param user_name: The username of the user whose home address is to be retrieved
SELECT home_address FROM users WHERE username = :user_name;

-- name: get_users_work_address^
-- Get the work address of a user
-- :param user_name: The username of the user whose work address is to be retrieved
SELECT work_address FROM users WHERE username = :user_name;

-- name: get_users_time_zone^
-- Get the time zone of a user
-- :param user_name: The username of the user whose time zone is to be retrieved
SELECT time_zone FROM users WHERE username = :user_name;

-- name: remove_user_from_db!
-- Remove a user from the users table
-- :param user_name: The username of the user to be removed
DELETE FROM users WHERE username = :user_name;
