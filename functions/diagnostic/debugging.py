"""
DESCRIPTION: Debugging functions reside here
"""
import io
import aiohttp
import aiofiles
import discord
import os
import logging
import time
import psutil

from discord.ext import commands
from functions.core.config import config
from functions.core.embeds import create_embed
from functions.core.utils import setup_logger, modal_error_check, get_bot_member

logger = setup_logger("diagnostic")
URL = "https://api.github.com/repos/aaron-rai/dollar-discord-bot/issues"
ACCESS_TOKEN = config.GITHUB_TOKEN


class GithubIssueModal(discord.ui.Modal):
	"""
	DESCRIPTION: Creates GitHub Issue Modal
	PARAMETERS: discord.ui.modal - Discord Modal
	"""

	def __init__(self, issue_type: str, title_label: str, desc_label: str, modal_title: str):
		super().__init__(title=modal_title)
		self.issue_type = issue_type
		self.title_label = discord.ui.TextInput(label=title_label, placeholder=f"Enter {issue_type} Title", required=True)
		self.desc_label = discord.ui.TextInput(
			label=desc_label, placeholder=f"Enter a detailed description of the {issue_type}", required=True
		)
		self.add_item(self.title_label)
		self.add_item(self.desc_label)

	@staticmethod
	async def _create_github_issue(title: str, body: str, author: str, server: str, issue_type: str) -> tuple[int, str]:
		"""
		DESCRIPTION: Create GitHub Issue
		PARAMETERS: title - Issue Title, body - Issue Body, author - Issue Author, server - Issue Server, type - Issue Type
		"""
		issue_body = f"{body}\n\nSubmitted by: {author}\nServer: {server}"
		payload = {"title": title, "body": issue_body, "labels": [issue_type]}

		headers = {"Authorization": f"token {ACCESS_TOKEN}"}

		async with aiohttp.ClientSession() as session:
			async with session.post(URL, headers=headers, json=payload) as response:
				status = response.status
				text = await response.text()
				return status, text

	async def on_submit(self, interaction: discord.Interaction):
		"""
		DESCRIPTION: Fires on submit of GitHub Issue Modal
		PARAMETERS: interaction - Discord Interaction
		"""
		status, text = await self._create_github_issue(
			self.title_label.value,
			self.desc_label.value,
			str(interaction.user),
			str(interaction.guild),
			self.issue_type,
		)
		if status == 201:
			logger.info(f"Added {self.issue_type} to GitHub issues")
			await interaction.response.send_message(f"{self.issue_type.capitalize()} submitted successfully.", ephemeral=True)
		else:
			await interaction.response.send_message(f"Failed to add {self.issue_type} to GitHub issues.", ephemeral=True)
			logger.error(f"Failed to add {self.issue_type} to GitHub issues: {text}")

	async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
		"""
		DESCRIPTION: Fires on error of GitHub Issue Modal
		PARAMETERS: discord.Interaction - Discord Interaction
		"""
		message = modal_error_check(error)
		await interaction.response.send_message(message, ephemeral=True)
		logger.error(f"An error occurred: {error}")


class ReportBugModel(GithubIssueModal):
	"""
	DESCRIPTION: Creates Report Bug Model
	PARAMETERS: discord.ui.modal - Discord Modal
	"""

	def __init__(self):
		super().__init__(
			modal_title="Report Bug",
			issue_type="bug",
			title_label="Bug Title",
			desc_label="Bug Description",
		)


class FeatureRequestModel(GithubIssueModal):
	"""
	DESCRIPTION: Creates Feature Request Model
	PARAMETERS: discord.ui.modal - Discord Modal
	"""

	def __init__(self):
		super().__init__(
			modal_title="Feature Request",
			issue_type="enhancement",
			title_label="Feature Title",
			desc_label="Feature Description",
		)


class HelpView(discord.ui.View):
	"""
	DESCRIPTION: Creates Help View
	PARAMETERS: discord.ui.View - Discord View
	"""

	def __init__(self):
		super().__init__()
		self.add_item(MyButton(label="Music", style=discord.ButtonStyle.green, custom_id="music"))
		self.add_item(MyButton(label="Context Menu", style=discord.ButtonStyle.blurple, custom_id="context"))
		self.add_item(MyButton(label="Slash", style=discord.ButtonStyle.red, custom_id="slash"))


class MyButton(discord.ui.Button):
	"""
	DESCRIPTION: Creates Button for Help View
	PARAMETERS: discord.ui.Button - Discord Button
	"""

	async def callback(self, interaction: discord.Interaction):
		"""
		DESCRIPTION: Fires on button click
		PARAMETERS: interaction - Discord Interaction
		"""
		dollar = await get_bot_member(interaction.guild, interaction.client)
		command_type = str(self.custom_id)

		if command_type:
			await interaction.message.edit(view=None)
			await self.send_commands(interaction, command_type, dollar)

	async def send_commands(self, interaction: discord.Interaction, command_type: str, dollar: discord.Member) -> None:
		"""
		DESCRIPTION: Send commands based on command type
		PARAMETERS: interaction - Discord Interaction, command_type - Command Type, dollar - Dollar Bot
		"""
		logger.debug(f"Sending {command_type} commands for user {interaction.user.name}")
		file_path = os.path.join("markdown", f"{command_type}Commands.md")
		try:
			async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
				dollar_commands = await file.read()
				embed = create_embed(f"{command_type.capitalize()} Commands", dollar_commands, dollar)
				await interaction.response.send_message(embed=embed)
		except FileNotFoundError:
			logger.error(f"File {file_path} not found")
		except Exception as e:
			logger.error(f"Failed to send commands: {e}")


class Debugging(commands.Cog):
	"""
	DESCRIPTION: Creates Debugging Class
	PARAMETERS: commands.Bot - Discord Commands
	"""

	def __init__(self, bot):
		self.bot = bot

	@discord.app_commands.command(name="status", description="Dollar server status, CPU usage, Memory usage, Uptime, etc.")
	async def status(self, interaction: discord.Interaction):
		"""
		DESCRIPTION: Check dollar diagnostics, CPU, RAM, Uptime
		PARAMETERS: interaction - Discord interaction
		"""
		uptime = time.time() - interaction.client.start_time
		uptime_days = uptime // (24 * 3600)
		uptime = uptime % (24 * 3600)
		uptime_hours = uptime // 3600
		uptime_minutes = (uptime % 3600) // 60
		uptime_seconds = uptime % 60
		uptime_formatted = f"{int(uptime_days)}d {int(uptime_hours)}h {int(uptime_minutes)}m {int(uptime_seconds)}s"
		cpu_percent = psutil.cpu_percent()
		ram_usage = psutil.virtual_memory().percent
		response_message = f"Uptime: {uptime_formatted}\nCPU Load: {cpu_percent}%\nRAM Usage: {ram_usage}%"
		await interaction.response.send_message(response_message)

	@discord.app_commands.command(name="reportbug", description="Report a bug to the developer")
	async def reportbug(self, interaction: discord.Interaction):
		"""
		DESCRIPTION: Submit a bug
		PARAMETERS: interaction - Discord interaction
		"""
		logger.info(f"Creating Report Bug Model for user {interaction.user.name}")
		await interaction.response.send_modal(ReportBugModel())

	@discord.app_commands.command(name="featurerequest", description="Submit a feature request to the developer")
	async def featurerequest(self, interaction: discord.Interaction):
		"""
		DESCRIPTION: Submit a feature request
		PARAMETERS: interaction - Discord interaction
		"""
		logger.info(f"Creating Feature Request Model for user {interaction.user.name}")
		await interaction.response.send_modal(FeatureRequestModel())

	@discord.app_commands.command(name="help", description="See available commands for Dollar")
	async def help(self, interaction: discord.Interaction):
		"""
		DESCRIPTION: Show available commands
		PARAMETERS: interaction - Discord interaction
		"""
		logger.info(f"Creating Help View for user {interaction.user.name}")
		await interaction.response.send_message("Which commands?", view=HelpView())

	@commands.command()
	@commands.is_owner()
	async def logs(self, ctx):
		"""
		DESCRIPTION: See Dollar's current logs
		PARAMETERS: ctx - Discord Context
		"""
		log_file_name = "discord.log"
		log_file_path = os.path.join(os.getcwd(), log_file_name)

		if not os.path.isfile(log_file_path):
			await ctx.send(f"Log file '{log_file_name}' not found.")
			return

		channel = ctx.channel
		async with aiofiles.open(log_file_path, "rb") as file:
			file_bytes = await file.read()
			log_file = discord.File(io.BytesIO(file_bytes), filename=log_file_name)
			await channel.send(file=log_file)

	@commands.command()
	@commands.is_owner()
	async def logging(self, ctx, level):
		"""
		DESCRIPTION: Set logging to certain level
		PARAMETERS: ctx - Discord Context, level - logging level
		"""
		level = getattr(logging, level.upper(), None)
		if level is None:
			await ctx.send("Invalid logging level provided.")
			return
		#pylint: disable=redefined-outer-name
		for name, logger in logging.root.manager.loggerDict.items():
			if isinstance(logger, logging.Logger):
				logger.info(f"Setting {name} to {level}")
				logger.setLevel(level)

		await ctx.send(f"Logging level set to {level}.")


async def setup(bot):
	await bot.add_cog(Debugging(bot))
