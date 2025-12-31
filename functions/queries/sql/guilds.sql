-- name: add_guild!
INSERT INTO guilds (guild_name, owner_id)
SELECT :guild_name, user_id FROM users
WHERE username = :user_name AND NOT EXISTS (
	SELECT 1 FROM guilds WHERE guild_name = :guild_name
);

-- name: check_guild_exists^
SELECT guild_name FROM guilds WHERE guild_name = :guild_name;

-- name: remove_guild_preferences!
DELETE FROM guild_preferences WHERE guild_id = (SELECT guild_id FROM guilds WHERE guild_name = :guild_name);

-- name: remove_guild!
DELETE FROM guilds WHERE guild_name = :guild_name;

-- name: add_guild_preferences!
INSERT INTO guild_preferences (text_channel, voice_channel, shows_channel, guild_id)
VALUES (:text_channel, :voice_channel, :shows_channel, (SELECT guild_id FROM guilds WHERE guild_name = :guild_name))
ON CONFLICT (guild_id) DO UPDATE SET
	text_channel = :text_channel,
	voice_channel = :voice_channel,
	shows_channel = :shows_channel;

-- name: get_guilds_preferred_text_channel^
SELECT text_channel FROM guild_preferences
WHERE guild_id = (SELECT guild_id FROM guilds WHERE guild_name = :guild_name);

-- name: get_guilds_preferred_voice_channel^
SELECT voice_channel FROM guild_preferences
WHERE guild_id = (SELECT guild_id FROM guilds WHERE guild_name = :guild_name);

-- name: get_guilds_preferred_shows_channel^
SELECT shows_channel FROM guild_preferences
WHERE guild_id = (SELECT guild_id FROM guilds WHERE guild_name = :guild_name);
