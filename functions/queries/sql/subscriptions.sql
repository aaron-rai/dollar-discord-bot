-- name: add_game_subscription!
-- Add a subscription for a user to a specific game
-- :param user_name: The username of the user subscribing to the game
-- :param game_name: The name of the game to subscribe to
INSERT INTO game_subscriptions (user_id, game_id)
VALUES ((SELECT user_id FROM users WHERE username = :user_name),
		(SELECT game_id FROM games WHERE game_name = :game_name));

-- name: get_game_subscriptions^
-- Retrieve a list of Discord IDs for users subscribed to a specific game
-- :param game_name: The name of the game whose subscribers are to be retrieved
SELECT discord_id FROM users WHERE user_id IN
	(SELECT user_id FROM game_subscriptions WHERE game_id =
		(SELECT game_id FROM games WHERE game_name = :game_name));

-- name: remove_game_subscription!
-- Remove a subscription for a user from a specific game
-- :param user_name: The username of the user unsubscribing from the game
-- :param game_name: The name of the game to unsubscribe from
DELETE FROM game_subscriptions WHERE user_id =
	(SELECT user_id FROM users WHERE username = :user_name) AND game_id =
	(SELECT game_id FROM games WHERE game_name = :game_name);
