-- name: add_game!
-- Add a new game to the games table
-- :param game_name: The name of the game to be added
INSERT INTO games (game_name)
VALUES (:game_name);

-- name: check_game_exists^
-- Check if a game exists in the games table
-- :param game_name: The name of the game to check for existence
SELECT game_name FROM games WHERE game_name = :game_name;