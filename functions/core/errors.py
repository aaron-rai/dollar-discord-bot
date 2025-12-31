"""
DESCRIPTION: Common error mappings for the bot
"""
import discord
import wavelink
from discord.ext import commands

ERROR_MAPPING = {
	commands.MissingRole: ("Missing Required Role", "User has insufficient role"),
	commands.CommandNotFound: ("Command Not Found", "User tried to use a command that does not exist"),
	commands.BadArgument: ("Invalid Argument", "User provided an invalid argument"),
	commands.CheckFailure: ("Incorrect Command Usage", "User used command incorrectly"),
	discord.errors.PrivilegedIntentsRequired: ("Missing Required Intent", "Bot is missing required intent"),
	commands.CommandOnCooldown: ("Command Cooldown", "Command on cooldown for user"),
	wavelink.LavalinkException: ("Lavalink Error", "Lavalink error occurred"),
	wavelink.InvalidChannelStateException: ("Invalid Channel State", "Invalid channel state"),
}
