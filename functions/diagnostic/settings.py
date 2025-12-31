"""
Dollar Customization Settings
"""
import discord

from discord.ext import commands
from functions.core.utils import setup_logger, modal_error_check, is_guild_owner_interaction

logger = setup_logger("settings")


class SettingsModal(discord.ui.Modal, title="DollarSettings"):
	"""
	DESCRIPTION: Creates Settings Modal
	PARAMETERS: discord.ui.Modal - Discord Modal
	"""

	def __init__(self, queries):
		super().__init__()
		self.queries = queries

	text_channel = discord.ui.TextInput(label="Text Channel", placeholder="Enter Preferred Text Channel Name", required=True)
	voice_channel = discord.ui.TextInput(label="Voice Channel", placeholder="Enter Preferred Voice Channel Name", required=True)
	shows_channel = discord.ui.TextInput(label="Shows Channel", placeholder="Enter Preferred Shows Channel Name", required=True)

	async def create_channels(self, guild, text_channel_value, voice_channel_value, shows_channel_value):
		"""
		DESCRIPTION: Creates text, voice, and shows channels if they do not already exist
		PARAMETERS: discord.Guild - Discord Guild, str - Text Channel Name, str - Voice Channel Name, str - Shows Channel Name
		"""
		logger.debug(f"Checking for existing channels and creating text, voice, and shows channels for guild {guild}")

		existing_channels = {channel.name: channel for channel in guild.channels}

		if text_channel_value not in existing_channels:
			await guild.create_text_channel(text_channel_value)
			logger.debug(f"Text channel '{text_channel_value}' created for guild {guild}")
		else:
			logger.warning(f"Text channel '{text_channel_value}' already exists in guild {guild}")

		if voice_channel_value not in existing_channels:
			await guild.create_voice_channel(voice_channel_value)
			logger.debug(f"Voice channel '{voice_channel_value}' created for guild {guild}")
		else:
			logger.warning(f"Voice channel '{voice_channel_value}' already exists in guild {guild}")

		if shows_channel_value not in existing_channels:
			await guild.create_voice_channel(shows_channel_value)
			logger.debug(f"Shows channel '{shows_channel_value}' created for guild {guild}")
		else:
			logger.warning(f"Shows channel '{shows_channel_value}' already exists in guild {guild}")

	async def on_submit(self, interaction: discord.Interaction):
		"""
		DESCRIPTION: Fires on submit of Settings Modal
		PARAMETERS: discord.Interaction - Discord Interaction
		"""
		guild_id = interaction.guild_id
		guild = interaction.guild
		guild_owner = interaction.guild.owner
		text_channel_value = self.text_channel.value.replace(" ", "-").lower()
		voice_channel_value = self.voice_channel.value
		shows_channel_value = self.shows_channel.value
		logger.debug(
			f"Guild ID: {guild_id}, Text Channel: {text_channel_value}, Voice Channel: {voice_channel_value}, Shows Channel: {shows_channel_value}"
		)

		result = self.queries.check_if_guild_exists(str(guild))
		if result:
			logger.debug(f"Guild {guild_id} exists in database, updating text, voice, and shows channels")
			self.queries.add_guild_preferences(text_channel_value, voice_channel_value, shows_channel_value, str(guild))
		else:
			logger.debug(f"Guild {guild_id} does not exist in database, adding text, voice, and shows channels")
			owner_exists = self.queries.check_if_user_exists(str(guild_owner))
			if owner_exists is None:
				self.queries.add_user_to_db(guild.owner.id, guild.owner.name)
			self.queries.add_guild_to_db(str(guild), str(guild_owner))
			self.queries.add_guild_preferences(text_channel_value, voice_channel_value, shows_channel_value, str(guild))

		#NOTE: Update text, voice channel caches
		bot = interaction.client
		bot.guild_text_channels[str(guild)] = text_channel_value
		bot.guild_voice_channels[str(guild)] = voice_channel_value
		logger.debug(f"Text and voice channel caches updated for guild {guild_id}")

		await interaction.response.send_message("Settings Saved! Creating your channels", ephemeral=True)

		await self.create_channels(guild, text_channel_value, voice_channel_value, shows_channel_value)
		logger.info(f"Dollar Settings saved for guild {guild_id}")

	async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
		"""
		DESCRIPTION: Fires on error of Settings Modal
		PARAMETERS: discord.Interaction - Discord Interaction
		"""
		message = modal_error_check(error)
		await interaction.response.send_message(message, ephemeral=True)
		logger.error(f"An error occurred: {error}")


class UserInfoModal(discord.ui.Modal, title="UserInfo"):
	"""
	DESCRIPTION: Creates UserInfo Modal
	PARAMETERS: discord.ui.Modal - Discord Modal
	"""

	def __init__(self, queries):
		super().__init__()
		self.queries = queries

	home_address = discord.ui.TextInput(label="Home Address", placeholder="Enter Home Address", required=True)
	work_address = discord.ui.TextInput(label="Work Address", placeholder="Enter Work Address", required=True)
	time_zone = discord.ui.TextInput(
		label="Time Zone", placeholder="Enter timezone (Eastern/Central/Mountain/Pacific)", required=True, max_length=8
	)

	async def on_submit(self, interaction: discord.Interaction):
		"""
		DESCRIPTION: Fires on submit of UserInfo Modal
		PARAMETERS: discord.Interaction - Discord Interaction
		"""
		user_name = interaction.user.name
		user_id = interaction.user.id
		home_address_value = self.home_address.value
		work_address_value = self.work_address.value
		timezone_value = self.time_zone.value.lower()

		valid_timezones = ["eastern", "central", "mountain", "pacific"]

		if timezone_value not in valid_timezones:
			await interaction.response.send_message(
				"Invalid timezone. Please use Eastern, Central, Mountain, or Pacific.", ephemeral=True
			)
			return

		logger.debug(
			f"Username: {user_name}, Home Address: {home_address_value}, Work Address: {work_address_value}, Time Zone: {timezone_value}"
		)

		user_exists = self.queries.check_if_user_exists(str(user_name))
		if user_exists is None:
			logger.debug("User does not exist in database")
			self.queries.add_user_to_db(user_id, user_name, home_address_value, work_address_value, timezone_value)
		else:
			logger.debug(f"User exists in database, updating home and work addresses for user {user_name}")
			self.queries.update_users_home_address(user_name, home_address_value)
			self.queries.update_users_work_address(user_name, work_address_value)
			self.queries.update_users_time_zone(user_name, timezone_value)
			logger.debug(f"Home, work addresses, and timezone updated for user {user_name}")
		await interaction.response.send_message(
			"Thanks! This data will never be shared and will be stored securely.", ephemeral=True
		)

	async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
		"""
		DESCRIPTION: Fires on error of Settings Modal
		PARAMETERS: discord.Interaction - Discord Interaction
		"""
		message = modal_error_check(error)
		await interaction.response.send_message(message, ephemeral=True)
		logger.error(f"An error occurred: {error}")


class Settings(commands.Cog):
	"""
	DESCRIPTION: Creates Settings class and commands
	PARAMETERS: commands.Bot - Discord
	"""

	def __init__(self, bot):
		self.bot = bot

	@discord.app_commands.command(name="dollarsettings", description="Change Dollar Settings")
	async def settings(self, interaction: discord.Interaction):
		"""
		DESCRIPTION: Creates Settings command
		PARAMETERS: discord.Interaction - Discord Interaction
		"""
		logger.debug(f"Creating Settings Modal for user: {interaction.user.name}")
		is_guild_owner = is_guild_owner_interaction()
		if not is_guild_owner:
			await interaction.response.send_message("You must be the server owner to change settings", ephemeral=True)
		else:
			# Get Queries cog instance
			queries_cog = self.bot.get_cog("Queries")
			await interaction.response.send_modal(SettingsModal(queries_cog))

	@discord.app_commands.command(name="updateuserinfo", description="Update Your User Information")
	async def userinformation(self, interaction: discord.Interaction):
		"""
		DESCRIPTION: Creates UserInfo command
		PARAMETERS: discord.Interaction - Discord Interaction
		"""
		logger.debug(f"Creating UserInfo Modal for: {interaction.user.name}")
		# Get Queries cog instance
		queries_cog = self.bot.get_cog("Queries")
		await interaction.response.send_modal(UserInfoModal(queries_cog))


async def setup(bot):
	await bot.add_cog(Settings(bot))
