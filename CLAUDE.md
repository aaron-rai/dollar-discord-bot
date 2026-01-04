# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dollar is a Discord bot that provides music playback (via Lavalink/Wavelink), moderation features, auto voice channel creation, and game update notifications. Built with discord.py and runs in Docker with PostgreSQL database and Lavalink audio server.

## Architecture

### Core Components

- **bot.py**: Main entry point containing UnfilteredBot class, event handlers, and bot lifecycle management
- **functions/**: Organized into specialized modules:
  - `core/`: Shared infrastructure (config, database, embeds, errors, utils, auto-channel creation)
  - `music/`: Music playback commands via Wavelink (CustomPlayer extends wavelink.Player)
  - `admin/`: Administrative/moderation commands
  - `diagnostic/`: Debugging and settings commands
  - `notifications/`: Push notifications for game updates
  - `queries/`: Database query operations
- **functions/core/**: Core infrastructure modules
  - `config.py`: Environment variable loading and configuration management
  - `database.py`: Connection pool management with context managers
  - `embeds.py`: Discord embed creation and patch note sending
  - `errors.py`: Central error mapping for user-friendly error messages
  - `utils.py`: Shared utility functions including logging setup

### Extension System

Bot uses discord.py's cog extension system. Extensions are loaded in bot.py:
```python
exts = [
    "functions.diagnostic.debugging",
    "functions.music.musiccommands",
    "functions.admin.admin",
    "functions.queries.queries",
    "functions.diagnostic.settings",
    "functions.notifications.push_notifications"
]
```

Extensions are loaded in `setup_hook()` and synced with Discord's API. Each cog is a Python class that extends `commands.Cog`.

### Database Schema

PostgreSQL with schema `dollar` containing:
- `users`: Discord users with optional location/timezone info
- `games`: Game titles for update notifications
- `game_subscriptions`: User subscriptions to game updates
- `guilds`: Discord servers using Dollar
- `guild_preferences`: Per-guild text/voice channel preferences (text_channel, voice_channel, shows_channel)

Guild-specific channel preferences are cached in `guild_text_channels` and `guild_voice_channels` dictionaries at startup in `on_ready()` event. Schema initialization happens automatically via `sql/init.sql` mounted as Docker entrypoint.

### Music System

Uses Wavelink to connect to Lavalink audio server. CustomPlayer (in `functions/music/player.py`) extends wavelink.Player with queue management. Lavalink runs in separate container (configured via application.yml) with YouTube plugin v1.16.0. YouTube source is disabled in favor of the plugin which supports multiple YouTube clients (MUSIC, WEB, ANDROID_MUSIC, IOS, TV, etc.) for better reliability.

### Logging

Structured logging system with named loggers per feature area:
- administrative, auto-channel-creation, core, diagnostic, dollar, game, music, notifications, queries, settings

All logs written to `discord.log` (rotating file handler, 1MB max, 5 backups). For debugging, always check `discord.log` rather than console output.

### Event Handling

Key events in bot.py:
- `on_guild_join/remove`: DB setup/cleanup for guilds
- `on_voice_state_update`: Auto channel creation when users join designated "JOIN HERE" channel
- `on_scheduled_event_update`: Manages voice channel permissions for scheduled events
- `on_raw_reaction_add`: Game notification subscriptions via bell emoji reactions
- `on_message`: Enforces command usage in designated text channels

## Development Commands

### Python Environment Setup

Install Python dependencies for local development:
```bash
cd scripts && pip install -r requirements.txt
```

Required packages: discord.py, wavelink, psycopg2, python-dotenv, lyricsgenius, spotipy, aiosql, pytz, psutil, requests

### Docker Development (Primary Method)

Build and run all services (bot, lavalink, postgres):
```bash
docker compose up -d
```

Rebuild after code changes:
```bash
docker compose up --build -d
```

Helper scripts for rebuild with cleanup:
```bash
./scripts/rebuild-and-prune.sh      # Linux
.\scripts\rebuild-and-prune.ps1     # Windows
```

View logs:
```bash
docker logs dollar          # Bot logs
docker logs lavalink        # Lavalink logs
docker logs postgres        # Database logs
```

### Linting

PyLint is required and runs on all pushes via GitHub Actions (`.github/workflows/pylint.yml`):
```bash
find . -name '*.py' ! -path "./deprecated/*" | xargs pylint
```

Configuration in `.pylintrc` (Google Python style guide based). Runs on Python 3.10 in CI.

### Documentation

Docusaurus site in `docs/`:
```bash
cd docs && npm install
npm start  # Preview at localhost:3000
```

Documentation is automatically deployed via GitHub Actions on pushes to main.

## Environment Configuration

Required variables in `.env` (see `.env.template`):
- Discord: TOKEN, CASH (developer ID)
- Lavalink: LAVALINK_TOKEN, LAVALINK_EMAIL, LAVALINK_PASSWORD
- Database: DB_USER, DB_PW, DB_SCHEMA
- API tokens: GENIUSTOKEN, CLIENT_ID/CLIENT_SECRET (Spotify), TRACKERGG, RIOTTOKEN, GHUBTOKEN
- Config: PATCHES_CHANNEL (game update channel ID), SEND_PATCH_NOTES (true/false)

## Coding Patterns

### Command Structure

Commands use discord.py's app_commands (slash commands). Each cog defines commands as methods decorated with `@app_commands.command()`.

### Error Handling

Central error mapping in `functions/core/errors.py` (ERROR_MAPPING dict) maps exception types to user-friendly messages. Maps discord.py command errors, Wavelink exceptions, and permission errors to human-readable titles and descriptions.

### Database Connections

Database connection managed via DatabaseService class (`functions/core/database.py`) using psycopg2 SimpleConnectionPool with:
- Retry logic: 5 attempts with exponential backoff (2s initial delay)
- Pool size: 1-8 connections
- Context managers: `get_connection()` and `get_cursor()` ensure proper cleanup
- Health check: `validate_db` task runs every 60s to test connection

**Important**: The `main` service in docker-compose.yml uses `depends_on` with `service_healthy` condition to ensure PostgreSQL is fully ready before the bot starts. The database healthcheck runs every 2s with 30 retries and 10s start period.

### Wavelink Integration

Lavalink node connects at startup in `connect_nodes()` called from `on_ready()` event. Configuration:
- Node URI: `http://lavalink:2333` (Docker internal networking)
- Identifier: "MAIN"
- Heartbeat: 60s
- Inactive player timeout: 600s (10 minutes)
- Cache capacity: 100 tracks
- Retries: unlimited (None)

## Important Notes

- Bot requires all Discord intents (`Intents.all()`)
- Command prefix is `!` but bot primarily uses slash commands (app_commands)
- Commands are synced globally with Discord's API during `setup_hook()`
- PATCHES_CHANNEL environment variable references a specific Discord channel for game update notifications
- Auto-channel creation tracks created channels to manage cleanup
- Patch notes are sent on startup if SEND_PATCH_NOTES=true
- All logs written to `discord.log` with 1MB rotation (5 backups)
- Docker containers use `America/Los_Angeles` timezone
- Database connection pool is shared across all cogs via singleton DatabaseService
- Bot startup sequence: load extensions → sync commands → connect to Wavelink → cache guild preferences → send patch notes (optional)
