"""
DESCRIPTION: Queries for the database reside here
"""
#pylint: disable=not-callable
import aiosql
from pathlib import Path
from functools import wraps
from discord.ext import commands
from psycopg2 import DatabaseError, Error, IntegrityError, ProgrammingError
from functions.core.utils import setup_logger
from functions.core.database import get_database_service

logger = setup_logger("queries")


def handle_exceptions(func):
	"""
	DESCRIPTION: Decorator to handle exceptions in database queries.
	Logs errors and re-raises them for proper error handling.
	PARAMETERS: func (obj) - Function to be wrapped
	"""

	@wraps(func)
	def wrapper(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except ProgrammingError as err:
			logger.error(f"Programming error in {func.__name__}: {err}")
			raise
		except IntegrityError as err:
			logger.error(f"Integrity error in {func.__name__}: {err}")
			raise
		except DatabaseError as err:
			logger.error(f"Database error in {func.__name__}: {err}")
			raise
		except Error as err:
			logger.error(f"General error in {func.__name__}: {err}")
			raise

	return wrapper


class Queries(commands.Cog):
	"""
	DESCRIPTION: Database query operations with proper connection pooling.
	PARAMETERS: commands.Bot - Discord Commands
	"""

	def __init__(self, bot):
		self.bot = bot
		self.db_service = get_database_service()
		# Load all queries from the sql folder
		self.queries = aiosql.from_path(Path(__file__).parent / "sql", "psycopg2")

	@handle_exceptions
	#pylint: disable=too-many-positional-arguments
	def add_user_to_db(self, user_id, user_name, home_address=None, work_address=None, time_zone=None):
		"""
		DESCRIPTION: Adds a user to the database

		PARAMETERS: user_id (str) - Discord user ID
					user_name (str) - Discord user name
					home_address (str, OPT) - Home address
					work_address (str, OPT) - Work address
					time_zone (str, OPT) - Timezone
		"""
		logger.debug("Executing query to add user")
		with self.db_service.get_connection() as conn:
			self.queries.add_user(
				conn, user_id=user_id, user_name=user_name, home_address=home_address, work_address=work_address,
				time_zone=time_zone
			)
		logger.debug("Query to add user executed")

	@handle_exceptions
	def check_if_user_exists(self, user_name):
		"""
		DESCRIPTION: Checks if a user exists in the database

		PARAMETERS: user_name (str) - Discord user name

		RETURNS: tuple or None - User record if exists, None otherwise
		"""
		logger.debug("Executing query to check if user exists")
		with self.db_service.get_connection() as conn:
			result = self.queries.check_user_exists(conn, user_name=user_name)
		logger.debug("Query to check if user exists executed")
		return result

	@handle_exceptions
	def add_game_to_db(self, game_name):
		"""
		DESCRIPTION: Adds a game to the database

		PARAMETERS: game_name (str) - Game name
		"""
		logger.debug("Inserting game into database")
		with self.db_service.get_connection() as conn:
			self.queries.add_game(conn, game_name=game_name)
		logger.debug("Game inserted into database")

	@handle_exceptions
	def check_if_game_exists(self, game_name):
		"""
		DESCRIPTION: Checks if a game exists in the database

		PARAMETERS: game_name (str) - Game name

		RETURNS: tuple or None - Game record if exists, None otherwise
		"""
		logger.debug("Executing query to check if game exists")
		with self.db_service.get_connection() as conn:
			result = self.queries.check_game_exists(conn, game_name=game_name)
		logger.debug("Query to check if game exists executed")
		return result

	@handle_exceptions
	def add_game_subscription(self, user_name, game_name):
		"""
		DESCRIPTION: Adds a game subscription to the database

		PARAMETERS: user_name (str) - Discord user name
					game_name (str) - Game name
		"""
		logger.debug("Executing query to add game subscription")
		with self.db_service.get_connection() as conn:
			self.queries.add_game_subscription(conn, user_name=user_name, game_name=game_name)
		logger.debug("Query to add game subscription executed")

	@handle_exceptions
	def get_game_subscriptions(self, game_name):
		"""
		DESCRIPTION: Gets all Discord IDs subscribed to a game

		PARAMETERS: game_name (str) - Game name

		RETURNS: list - Discord IDs of subscribed users
		"""
		logger.debug("Executing query to get game subscriptions")
		with self.db_service.get_connection() as conn:
			result = self.queries.get_game_subscriptions(conn, game_name=game_name)
		logger.debug("Query to get game subscriptions executed")
		# aiosql returns a list of Row objects, extract discord_id from each
		discord_ids = [row[0] for row in result]
		return discord_ids

	@handle_exceptions
	def remove_game_subscription(self, user_name, game_name):
		"""
		DESCRIPTION: Removes a game subscription from the database

		PARAMETERS: user_name (str) - Discord user name
					game_name (str) - Game name
		"""
		logger.debug("Executing query to remove game subscription")
		with self.db_service.get_connection() as conn:
			self.queries.remove_game_subscription(conn, user_name=user_name, game_name=game_name)
		logger.debug("Query to remove game subscription executed")

	@handle_exceptions
	def update_users_home_address(self, user_name, home_address):
		"""
		DESCRIPTION: Updates a users home address in the database

		PARAMETERS: user_name (str) - Discord user name
					home_address (str) - Home address
		"""
		logger.debug("Executing query to update users home address")
		with self.db_service.get_connection() as conn:
			self.queries.update_users_home_address(conn, home_address=home_address, user_name=user_name)
		logger.debug("Query to update users home address executed")

	@handle_exceptions
	def update_users_work_address(self, user_name, work_address):
		"""
		DESCRIPTION: Updates a users work address in the database

		PARAMETERS: user_name (str) - Discord user name
					work_address (str) - Work address
		"""
		logger.debug("Executing query to update users work address")
		with self.db_service.get_connection() as conn:
			self.queries.update_users_work_address(conn, work_address=work_address, user_name=user_name)
		logger.debug("Query to update users work address executed")

	@handle_exceptions
	def update_users_time_zone(self, user_name, time_zone):
		"""
		DESCRIPTION: Updates a users time zone in the database

		PARAMETERS: user_name (str) - Discord user name
					time_zone (str) - Time zone
		"""
		logger.debug("Executing query to update users time zone")
		with self.db_service.get_connection() as conn:
			self.queries.update_users_time_zone(conn, time_zone=time_zone, user_name=user_name)
		logger.debug("Query to update users time zone executed")

	@handle_exceptions
	def get_users_home_address(self, user_name):
		"""
		DESCRIPTION: Gets a users home address from the database

		PARAMETERS: user_name (str) - Discord user name

		RETURNS: tuple or None - Address if exists, None otherwise
		"""
		logger.debug("Executing query to get users home address")
		with self.db_service.get_connection() as conn:
			result = self.queries.get_users_home_address(conn, user_name=user_name)
		logger.debug("Query to get users home address executed")
		return result

	@handle_exceptions
	def get_users_work_address(self, user_name):
		"""
		DESCRIPTION: Gets a users work address from the database

		PARAMETERS: user_name (str) - Discord user name

		RETURNS: tuple or None - Address if exists, None otherwise
		"""
		logger.debug("Executing query to get users work address")
		with self.db_service.get_connection() as conn:
			result = self.queries.get_users_work_address(conn, user_name=user_name)
		logger.debug("Query to get users work address executed")
		return result

	@handle_exceptions
	def get_users_time_zone(self, user_name):
		"""
		DESCRIPTION: Gets a users time zone from the database

		PARAMETERS: user_name (str) - Discord user name

		RETURNS: tuple or None - Time zone if exists, None otherwise
		"""
		logger.debug("Executing query to get users time zone")
		with self.db_service.get_connection() as conn:
			result = self.queries.get_users_time_zone(conn, user_name=user_name)
		logger.debug("Query to get users time zone executed")
		return result

	@handle_exceptions
	def remove_user_from_db(self, user_name):
		"""
		DESCRIPTION: Removes a user from the database

		PARAMETERS: user_name (str) - Discord user name
		"""
		logger.debug("Executing query to remove user")
		with self.db_service.get_connection() as conn:
			self.queries.remove_user_from_db(conn, user_name=user_name)
		logger.debug("Query to remove user executed")

	@handle_exceptions
	def add_guild_to_db(self, guild_name, user_name):
		"""
		DESCRIPTION: Adds a guild to the database

		PARAMETERS: guild_name (str) - Guild name
					user_name (str) - Discord user name
		"""
		logger.debug("Executing query to add guild")
		with self.db_service.get_connection() as conn:
			self.queries.add_guild(conn, guild_name=guild_name, user_name=user_name)
		logger.debug("Query to add guild executed")

	@handle_exceptions
	def check_if_guild_exists(self, guild_name):
		"""
		DESCRIPTION: Checks if a guild exists in the database

		PARAMETERS: guild_name (str) - Guild name

		RETURNS: tuple or None - Guild record if exists, None otherwise
		"""
		logger.debug("Executing query to check if guild exists")
		with self.db_service.get_connection() as conn:
			result = self.queries.check_guild_exists(conn, guild_name=guild_name)
		logger.debug("Query to check if guild exists executed")
		return result

	@handle_exceptions
	def remove_guild_from_db(self, guild_name):
		"""
		DESCRIPTION: Removes a guild from the database

		PARAMETERS: guild_name (str) - Guild name
		"""
		logger.debug("Executing query to remove guild")
		with self.db_service.get_connection() as conn:
			# Delete guild preferences first (foreign key constraint)
			self.queries.remove_guild_preferences(conn, guild_name=guild_name)
			logger.debug("Query to remove guild preferences executed")
			# Delete guild
			self.queries.remove_guild(conn, guild_name=guild_name)
			logger.debug("Query to remove guild executed")

	@handle_exceptions
	def add_guild_preferences(self, text_channel, voice_channel, shows_channel, guild_name):
		"""
		DESCRIPTION: Adds guild preferences to the database

		PARAMETERS: text_channel (str) - Text channel name
					voice_channel (str) - Voice channel name
					shows_channel (str) - Shows channel name
					guild_name (str) - Guild name
		"""
		logger.debug("Executing query to add guild preferences")
		with self.db_service.get_connection() as conn:
			self.queries.add_guild_preferences(
				conn, text_channel=text_channel, voice_channel=voice_channel, shows_channel=shows_channel,
				guild_name=guild_name
			)
		logger.debug("Query to add guild preferences executed")

	@handle_exceptions
	def get_guilds_preferred_text_channel(self, guild_name):
		"""
		DESCRIPTION: Gets the preferred text channel for a guild

		PARAMETERS: guild_name (str) - Guild name

		RETURNS: str or None - Text channel name if exists, None otherwise
		"""
		logger.debug("Executing query to get guilds preferred text channel")
		with self.db_service.get_connection() as conn:
			result = self.queries.get_guilds_preferred_text_channel(conn, guild_name=guild_name)
		logger.debug("Query to get guilds preferred text channel executed")
		return result[0] if result else None

	@handle_exceptions
	def get_guilds_preferred_voice_channel(self, guild_name):
		"""
		DESCRIPTION: Gets the preferred voice channel for a guild

		PARAMETERS: guild_name (str) - Guild name

		RETURNS: str or None - Voice channel name if exists, None otherwise
		"""
		logger.debug("Executing query to get guilds preferred voice channel")
		with self.db_service.get_connection() as conn:
			result = self.queries.get_guilds_preferred_voice_channel(conn, guild_name=guild_name)
		logger.debug("Query to get guilds preferred voice channel executed")
		return result[0] if result else None

	@handle_exceptions
	def get_guilds_preferred_shows_channel(self, guild_name):
		"""
		DESCRIPTION: Gets the preferred shows channel for a guild

		PARAMETERS: guild_name (str) - Guild name

		RETURNS: str or None - Shows channel name if exists, None otherwise
		"""
		logger.debug("Executing query to get guilds preferred shows channel")
		with self.db_service.get_connection() as conn:
			result = self.queries.get_guilds_preferred_shows_channel(conn, guild_name=guild_name)
		logger.debug("Query to get guilds preferred shows channel executed")
		return result[0] if result else None


async def setup(bot):
	await bot.add_cog(Queries(bot))
