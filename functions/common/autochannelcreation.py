"""
DESCRIPTION: Functions for Auto Channel Creation resides here
"""
#pylint: disable=not-async-context-manager
from ..common.generalfunctions import GeneralFunctions
from ..common import libraries as lib

logger = GeneralFunctions.setup_logger("auto-channel-creation")


class AutoChannelCreation():
	"""
	DESCRIPTION: Creates Auto Channel Creation Class
	"""

	def __init__(self):
		pass

	async def create_personal_channel(member, join_channel):
		"""
		DESCRIPTION: Creates a personal channel for a member
		PARAMETERS: member - discord.Member
					join_channel - discord
		RETURNS: None
		"""
		logger.debug(f"Starting channel creation for {member.display_name} in {member.guild.name}")

		@lib.asynccontextmanager
		async def lock_channel(channel):
			"""
			DESCRIPTION: Locks a channel
			PARAMETERS: channel - discord.VoiceChannel
			RETURNS: None
			"""
			try:
				await channel.set_permissions(channel.guild.default_role, connect=False)
				yield
			finally:
				await channel.set_permissions(channel.guild.default_role, connect=True)

		guild = member.guild
		category = join_channel.category
		trigger_channel_pos = join_channel.position

		async with lock_channel(join_channel):
			new_channel = await guild.create_voice_channel(
				f"{member.display_name}'s Channel", category=category, bitrate=96000, position=trigger_channel_pos
			)
			await new_channel.set_permissions(member, manage_channels=True)
			lib.created_channels.add(new_channel.id)

			await member.move_to(new_channel)
			await lib.asyncio.sleep(1)  # Short delay to ensure move completes

			logger.info(f"Created channel {new_channel.name} for {member.display_name} in {guild.name}")

			#NOTE: Check if member joined the channel if not delete the channel
			if not member.voice or member.voice.channel != new_channel:
				await new_channel.delete()
				logger.warning(
					f"User did not join voice channle, deleted orphaned channel {new_channel.name} in {guild.name}"
				)
				return

	async def handle_channel_leave(channel):
		"""
		DESCRIPTION: Handles channel leave event
		PARAMETERS: channel - discord.VoiceChannel
		RETURNS: None
		"""
		if channel.id in lib.created_channels and len(channel.members) == 0:
			await channel.delete()
			lib.created_channels.remove(channel.id)
			logger.info(f"Deleted empty channel {channel.name} in {channel.guild.name}")

	def get_join_channel(guild):
		"""
		DESCRIPTION: Gets trigger join channel for a guild
		PARAMETERS: guild - discord.Guild
		RETURNS: discord.VoiceChannel
		"""
		guild_saved_channel = lib.guild_voice_channels.get(str(guild))
		if not guild_saved_channel:
			guild_saved_channel = "JOIN HERE💎"
		return lib.discord.utils.get(guild.voice_channels, name=guild_saved_channel)
