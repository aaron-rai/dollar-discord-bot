-- name: add_guild!
-- Add a new guild to the guilds table
-- :param guild_name: The name of the guild to be added
-- :param user_name: The username of the guild owner
INSERT INTO guilds (guild_name, owner_id)
SELECT :guild_name, user_id FROM users
WHERE username = :user_name AND NOT EXISTS (
	SELECT 1 FROM guilds WHERE guild_name = :guild_name
);

-- name: check_guild_exists^
-- Check if a guild exists in the guilds table
-- :param guild_name: The name of the guild to check for existence
SELECT guild_name FROM guilds WHERE guild_name = :guild_name;

-- name: remove_guild_preferences!
-- Remove guild preferences for a specific guild
-- :param guild_name: The name of the guild whose preferences are to be removed
DELETE FROM guild_preferences WHERE guild_id = (SELECT guild_id FROM guilds WHERE guild_name = :guild_name);

-- name: remove_guild!
-- Remove a guild from the guilds table
-- :param guild_name: The name of the guild to be removed
DELETE FROM guilds WHERE guild_name = :guild_name;

-- name: add_guild_preferences!
-- Add or update guild preferences for a specific guild
-- :param guild_name: The name of the guild whose preferences are to be set
-- :param text_channel: The preferred text channel ID
-- :param voice_channel: The preferred voice channel ID
-- :param shows_channel: The preferred shows channel ID
INSERT INTO guild_preferences (text_channel, voice_channel, shows_channel, guild_id)
VALUES (:text_channel, :voice_channel, :shows_channel, (SELECT guild_id FROM guilds WHERE guild_name = :guild_name))
ON CONFLICT (guild_id) DO UPDATE SET
	text_channel = :text_channel,
	voice_channel = :voice_channel,
	shows_channel = :shows_channel;

-- name: get_guilds_preferred_text_channel^
-- Get the preferred text channel for a guild
-- :param guild_name: The name of the guild whose preferred text channel is to be retrieved
SELECT text_channel FROM guild_preferences
WHERE guild_id = (SELECT guild_id FROM guilds WHERE guild_name = :guild_name);

-- name: get_guilds_preferred_voice_channel^
-- Get the preferred voice channel for a guild
-- :param guild_name: The name of the guild whose preferred voice channel is to be retrieved
SELECT voice_channel FROM guild_preferences
WHERE guild_id = (SELECT guild_id FROM guilds WHERE guild_name = :guild_name);

-- name: get_guilds_preferred_shows_channel^
-- Get the preferred shows channel for a guild
-- :param guild_name: The name of the guild whose preferred shows channel is to be retrieved
SELECT shows_channel FROM guild_preferences
WHERE guild_id = (SELECT guild_id FROM guilds WHERE guild_name = :guild_name);
