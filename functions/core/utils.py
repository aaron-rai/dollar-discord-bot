"""
DESCRIPTION: Common utility functions used across the bot
"""
import discord
import logging
import logging.handlers
import pytz

from datetime import datetime
from discord.ext import commands


def setup_logger(logger_name: str) -> logging.Logger:
	"""
	Set up and configure a rotating file logger and stdout logger for the specified logger name.

	Parameters:
	- logger_name (str): The name of the logger.

	Returns:
	- logging.Logger: The configured logger instance.
	"""
	configured_logger = logging.getLogger(logger_name)

	if not configured_logger.handlers:
		#NOTE: File Handler (Rotating)
		file_handler = logging.handlers.RotatingFileHandler(
			filename="discord.log",
			encoding="utf-8",
			maxBytes=1024 * 1024,
			backupCount=5,
		)
		file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))

		#NOTE: Console Handler (stdout)
		console_handler = logging.StreamHandler()
		console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))

		configured_logger.addHandler(file_handler)
		configured_logger.addHandler(console_handler)
		configured_logger.setLevel(logging.INFO)

	return configured_logger


def convert_time_zone(time_str: str, time_zone: str) -> str:
	"""
	Convert the time to the specified timezone.

	Parameters:
	- time_str (str): The time to convert (format: "Month DD, YYYY at HH:MM AM/PM")
	- time_zone (str): The timezone to convert to (Eastern/Central/Mountain/Pacific)

	Returns:
	- str: The converted time in the same format
	"""
	timezone_map = {
		"eastern": "America/New_York",
		"central": "America/Chicago",
		"mountain": "America/Denver",
		"pacific": "America/Los_Angeles"
	}

	try:
		time_obj = datetime.strptime(time_str, "%B %d, %Y at %I:%M %p")
		target_tz = pytz.timezone(timezone_map[time_zone.lower()])
		utc_time = pytz.utc.localize(time_obj)
		converted_time = utc_time.astimezone(target_tz)
		return converted_time.strftime("%B %d, %Y at %I:%M %p")

	except ValueError:
		return "Error: Invalid time format. Expected format: Month DD, YYYY at HH:MM AM/PM"
	except KeyError:
		return "Error: Invalid timezone. Use Eastern, Central, Mountain, or Pacific"


async def get_bot_member(guild: discord.Guild, bot: discord.Client) -> discord.Member:
	"""
	Get the bot instance as a discord.Member object in a specific guild.
	
	Parameters:
	- guild: The guild to get the bot member from.
	- bot: The bot client.

	Returns:
	- discord.Member: The bot instance as a discord.Member object.
	"""
	return guild.get_member(bot.user.id)


def modal_error_check(error: Exception) -> str:
	"""
	DESCRIPTION: Fires on error of Settings Modal
	PARAMETERS: error - Exception
	"""
	if isinstance(error, discord.NotFound):
		message = "Oops! The item you were looking for was not found. Please report this bug using /reportbug."
	elif isinstance(error, discord.Forbidden):
		message = "Oops! I don't have permission to do that. Please report this bug using /reportbug."
	elif isinstance(error, discord.HTTPException):
		message = "Oops! Something went wrong with the Discord server. Please report this bug using /reportbug."
	else:
		message = "Oops! Something went wrong. Please report this bug using /reportbug."

	return message


def is_guild_owner() -> commands.check:
	"""
	Check if the command invoker is the guild owner. CTX Context.

	Returns:
	- A check function that raises `commands.CheckFailure`
	"""

	async def predicate(ctx):
		if not ctx.author.id == ctx.guild.owner_id:
			raise commands.CheckFailure("You need to be the guild owner to use this command")
		return True

	return commands.check(predicate)


def is_guild_owner_interaction() -> discord.app_commands.check:
	"""
	Check if the command invoker is the guild owner. Interaction Context.

	Returns:
	- A check function that raises `app_commands.CheckFailure`
	"""

	async def predicate(interaction: discord.Interaction) -> bool:
		if interaction.user.id != interaction.guild.owner_id:
			raise discord.app_commands.CheckFailure("You need to be the guild owner to use this command.")
		return True

	return discord.app_commands.check(predicate)
