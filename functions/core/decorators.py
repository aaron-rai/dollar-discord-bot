"""
DESCRIPTION: Common decorators for the bot.
"""

from discord.ext import commands


def is_connected_to_same_voice() -> commands.check:
	"""
	Check if the command invoker is connected to the same voice channel.

	Returns:
	- A check function that raises `commands.CheckFailure`
	"""

	async def predicate(ctx):
		if not ctx.author.voice:
			raise commands.CheckFailure("You need to be in a voice channel to use this command")
		elif not ctx.voice_client or ctx.author.voice.channel != ctx.voice_client.channel:
			raise commands.CheckFailure("You need to be in the same voice channel as Dollar to use this command")
		return True

	return commands.check(predicate)


def is_connected_to_voice() -> commands.check:
	"""
	Check if the command invoker is connected to a voice channel.

	Returns:
	- A check function that raises `commands.CheckFailure`
	"""

	async def predicate(ctx):
		if not ctx.author.voice:
			raise commands.CheckFailure("You need to be in a voice channel to use this command")
		return True

	return commands.check(predicate)
