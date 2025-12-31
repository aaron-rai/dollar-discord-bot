"""
DESCRIPTION: Common player class for Wavelink players.
"""
import wavelink


class CustomPlayer(wavelink.Player):
	"""
	DESCRIPTION: Creates CustomPlayer class for wavelink
	PARAMETERS: wavelink.Player - Player instance
	"""

	def __init__(self):
		super().__init__()
		self.queue = wavelink.Queue()
