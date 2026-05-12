"""
DESCRIPTION: Configuration settings for the application.
Defines constants and loads environment variables for use across the codebase.
"""

import os

# pylint: disable=invalid-name
# Config attribute use UPPER_CASE by convention, not lower_case


class Config():
	"""Application configuration loaded from environment variables."""

	# Discord
	DISCORD_TOKEN: str
	DEVELOPER: str

	# Spotify
	CLIENT_ID: str
	CLIENT_SECRET: str

	# Apis
	GITHUB_TOKEN: str
	GENIUS_TOKEN: str

	# Database
	DB_USER: str
	DB_PASSWORD: str
	DB_HOST: str
	DB_PORT: str
	DB_SCHEMA: str

	# Lavalink
	LAVALINK_TOKEN: str
	LAVALINK_EMAIL: str
	LAVALINK_PASSWORD: str

	# Features
	SEND_PATCH_NOTES: bool
	PATCHES_CHANNEL: int

	def __init__(self):
		"""Load and validate configuration from environment variables."""
		# Discord
		self.DISCORD_TOKEN = self._require("TOKEN")
		self.DEVELOPER = self._require("CASH")
		# Spotify
		self.CLIENT_ID = self._require("CLIENT_ID")
		self.CLIENT_SECRET = self._require("CLIENT_SECRET")
		# APIs
		self.GITHUB_TOKEN = self._require("GHUBTOKEN")
		self.GENIUS_TOKEN = self._require("GENIUSTOKEN")
		# Database
		self.DB_USER = self._require("DB_USER")
		self.DB_PASSWORD = self._require("DB_PW")
		self.DB_HOST = os.getenv("DB_HOST", "db")
		self.DB_PORT = int(os.getenv("DB_PORT", "5432"))
		self.DB_SCHEMA = self._require("DB_SCHEMA")
		# Lavalink
		self.LAVALINK_TOKEN = self._require("LAVALINK_TOKEN")
		self.LAVALINK_EMAIL = self._require("LAVALINK_EMAIL")
		self.LAVALINK_PASSWORD = self._require("LAVALINK_PASSWORD")
		# Features
		self.SEND_PATCH_NOTES = os.getenv("SEND_PATCH_NOTES", "").lower() == "true"
		patches_channel = os.getenv("PATCHES_CHANNEL")
		try:
			self.PATCHES_CHANNEL = int(patches_channel)
		except ValueError:
			self.PATCHES_CHANNEL = None
		# Version
		self.VERSION = "2.0.6"

	@staticmethod
	def _require(var_name: str) -> str:
		"""Retrieve an environment variable or raise an error if not found."""
		value = os.getenv(var_name)
		if value is None:
			raise EnvironmentError(f"Required environment variable '{var_name}' is not set.")
		return value

	@property
	def database_url(self) -> str:
		"""Construct the database connection URL."""
		return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_SCHEMA}"


config = Config()
