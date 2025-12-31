"""
DESCRIPTION: Functions for Auto Channel Creation resides here
"""
#pylint: disable=not-async-context-manager
import asyncio
import discord

from contextlib import asynccontextmanager
from functions.core.utils import setup_logger

logger = setup_logger("auto-channel-creation")


class AutoChannelCreation():
	"""
	DESCRIPTION: Creates Auto Channel Creation Class
	"""

	created_channels = set()

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

		@asynccontextmanager
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
			AutoChannelCreation.created_channels.add(new_channel.id)

			await member.move_to(new_channel)
			await asyncio.sleep(1)  # Short delay to ensure move completes

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
		if channel.id in AutoChannelCreation.created_channels and len(channel.members) == 0:
			await channel.delete()
			AutoChannelCreation.created_channels.remove(channel.id)
			logger.info(f"Deleted empty channel {channel.name} in {channel.guild.name}")

	def get_join_channel(guild, bot):
		"""
		DESCRIPTION: Gets trigger join channel for a guild
		PARAMETERS: guild - discord.Guild
					bot - discord.Client
		RETURNS: discord.VoiceChannel
		"""
		guild_saved_channel = bot.guild_voice_channels.get(str(guild))
		if not guild_saved_channel:
			guild_saved_channel = "JOIN HERE💎"
		return discord.utils.get(guild.voice_channels, name=guild_saved_channel)
