-- name: add_game!
INSERT INTO games (game_name)
VALUES (:game_name);

-- name: check_game_exists^
SELECT game_name FROM games WHERE game_name = :game_name;