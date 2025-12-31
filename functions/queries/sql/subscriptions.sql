-- name: add_game_subscription!
INSERT INTO game_subscriptions (user_id, game_id)
VALUES ((SELECT user_id FROM users WHERE username = :user_name),
		(SELECT game_id FROM games WHERE game_name = :game_name));

-- name: get_game_subscriptions^
SELECT discord_id FROM users WHERE user_id IN
	(SELECT user_id FROM game_subscriptions WHERE game_id =
		(SELECT game_id FROM games WHERE game_name = :game_name));

-- name: remove_game_subscription!
DELETE FROM game_subscriptions WHERE user_id =
	(SELECT user_id FROM users WHERE username = :user_name) AND game_id =
	(SELECT game_id FROM games WHERE game_name = :game_name);
