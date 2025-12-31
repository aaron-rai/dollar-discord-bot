"""
DESCRIPTION: Common embed creation functions for the bot.
"""
import discord
import os

from functions.core.utils import setup_logger
from functions.core.config import config

logger = setup_logger("embeds")


async def send_embed(title: str, image: str, msg: str, channel: discord.TextChannel, footer: bool = False) -> None:
	"""
	Send an embedded message with a title, image, and description to a specified channel.

	Parameters:
	- title (str): The title of the embed.
	- image (str): The filename of the image to be attached.
	- msg (str): The description or content of the embed.
	- channel (discord.TextChannel): The channel where the embed will be sent.
	- footer (bool): Flag to include a footer on embed.

	Returns:
	- None
	"""
	embed = discord.Embed(title=title, description=msg, color=discord.Color.random())
	embed.set_author(name="Dollar")
	file_path = os.path.join("images", image)
	img = discord.File(file_path, filename=image)
	embed.set_thumbnail(url=f"attachment://{image}")
	if footer:
		embed.set_footer(text="Feature request? Bug? Please report it by using `/reportbug` or `/featurerequest`")
	await channel.send(embed=embed, file=img)


async def send_embed_error(title: str, msg: str, channel: discord.TextChannel, footer: bool = False) -> None:
	"""
	Send an embedded error message with a title and description to a specified channel.

	Parameters:
	- title (str): The title of the error embed.
	- msg (str): The description or content of the error embed.
	- channel (discord.TextChannel): The channel where the error embed will be sent.
	- footer (bool): Flag to include a footer on embed.

	Returns:
	- None
	"""
	image = "error.png"
	embed = discord.Embed(title=title, description=msg, colour=0xe74c3c)
	embed.set_author(name="Dollar")
	file_path = os.path.join("images", image)
	img = discord.File(file_path, filename=image)
	embed.set_thumbnail(url=f"attachment://{image}")
	if footer:
		embed.set_footer(text="Feature request? Bug? Please report it by using `/reportbug` or `/featurerequest`")
	await channel.send(embed=embed, file=img)


def create_embed(title: str, description: str, author: discord.Member, image: str = "", footer: str = "") -> discord.Embed:
	"""
		Create an embedded message with a title, description, author, and footer.

		Parameters:
		- title (str): The title of the embed.
		- description (str): The description or content of the embed.
		- author (discord.Member): The author of the embed.
		- image (str): The filename of the image to be attached.
		- footer (str): The footer of the embed.

		Returns:
		- discord.Embed: The embed object.
		"""
	logger.debug(f"Creating embed with title: {title}, description: {description}, author: {author}, footer: {footer}")
	embed = discord.Embed(title=title, description=description, colour=0x2ecc71)
	embed.set_author(name=author, icon_url=author.avatar.url)
	if image:
		embed.set_thumbnail(url=image)
	if footer:
		embed.set_footer(text=footer)
	logger.debug("Embed created successfully, returning...")
	return embed


async def send_patch_notes(client: discord.Client) -> None:
	"""
	Send the latest patch notes to the system channel of each guild the bot is a member of.

	Parameters:
	- client (discord.Client): The Discord client instance representing the bot.

	Returns:
	- None
	"""

	async def send_patch_note_embed(channel, guild):
		"""
		Local function to send an embedded message with the latest patch notes to a specified channel.

		Parameters:
		- channel (discord.TextChannel): The channel where the embed will be sent.
		- guild (discord.Guild): The guild (server) associated with the channel.
		"""
		try:
			desc = ""
			file_path = os.path.join("markdown", "patch_notes.md")
			if os.path.isfile(file_path):
				with open(file_path, "r", encoding="utf-8") as file:
					desc = file.read()

			embed = discord.Embed(
				title=f"Version: {config.VERSION}", url="https://github.com/aaron-rai/dollar-discord-bot", description=desc,
				colour=discord.Color.green()
			)
			embed.set_author(name="Dollar")
			file_path = os.path.join("images", "dollar.png")
			img = discord.File(file_path, filename="dollar.png")
			embed.set_thumbnail(url="attachment://dollar.png")
			embed.set_footer(text="Feature request? Bug? Please report it by using `/reportbug` or `/featurerequest`")

			await channel.send(embed=embed, file=img)
			logger.debug(f"Notified {guild.name} of dollar's latest update.")
		except discord.Forbidden:
			logger.warning(f"Could not send message to {channel.name} in {guild.name}. Missing permissions.")
		except discord.HTTPException:
			logger.error(f"Could not send message to {channel.name} in {guild.name}. HTTP exception occurred.")

	for guild in client.guilds:
		logger.debug(f"Dollar loaded in {guild.name}, owner: {guild.owner}")
		channel = guild.system_channel
		if channel is not None:
			await send_patch_note_embed(channel, guild)
		else:
			for channel in guild.text_channels:
				if channel.name == "commands":
					await send_patch_note_embed(channel, guild)
