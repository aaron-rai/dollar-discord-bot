-- name: add_user!
INSERT INTO users (discord_id, username, home_address, work_address, time_zone)
VALUES (:user_id, :user_name, :home_address, :work_address, :time_zone);

-- name: check_user_exists^
SELECT username FROM users WHERE username = :user_name;

-- name: update_users_home_address!
UPDATE users SET home_address = :home_address WHERE username = :user_name;

-- name: update_users_work_address!
UPDATE users SET work_address = :work_address WHERE username = :user_name;

-- name: update_users_time_zone!
UPDATE users SET time_zone = :time_zone WHERE username = :user_name;

-- name: get_users_home_address^
SELECT home_address FROM users WHERE username = :user_name;

-- name: get_users_work_address^
SELECT work_address FROM users WHERE username = :user_name;

-- name: get_users_time_zone^
SELECT time_zone FROM users WHERE username = :user_name;

-- name: remove_user_from_db!
DELETE FROM users WHERE username = :user_name;
