# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dollar is a Discord bot that provides music playback (via Lavalink/Wavelink), moderation features, auto voice channel creation, and game update notifications. Built with discord.py and runs in Docker with PostgreSQL database and Lavalink audio server.

## Architecture

### Core Components

- **bot.py**: Main entry point containing UnfilteredBot class, event handlers, and bot lifecycle management
- **functions/**: Organized into specialized modules:
  - `common/`: Shared utilities (GeneralFunctions, AutoChannelCreation)
  - `music/`: Music playback commands via Wavelink
  - `admin/`: Administrative/moderation commands
  - `diagnostic/`: Debugging and settings commands
  - `game/`: Game-related commands
  - `notifications/`: Push notifications for game updates
  - `queries/`: Database query operations
- **functions/common/libraries.py**: Central import hub for all dependencies, global variables, and environment configuration

### Extension System

Bot uses discord.py's cog extension system. Extensions are loaded in bot.py:
```python
exts = [
    "functions.diagnostic.debugging",
    "functions.game.gamecommands",
    "functions.music.musiccommands",
    "functions.admin.admin",
    "functions.queries.queries",
    "functions.diagnostic.settings",
    "functions.notifications.push_notifications"
]
```

### Database Schema

PostgreSQL with schema `dollar` containing:
- `users`: Discord users with optional location/timezone info
- `games`: Game titles for update notifications
- `game_subscriptions`: User subscriptions to game updates
- `guilds`: Discord servers using Dollar
- `guild_preferences`: Per-guild text/voice channel preferences

Guild-specific channel preferences are cached in `guild_text_channels` and `guild_voice_channels` dictionaries at startup.

### Music System

Uses Wavelink to connect to Lavalink audio server. CustomPlayer extends wavelink.Player with queue management. Lavalink runs in separate container (configured via application.yml) with YouTube plugin support.

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

### Docker Development (Primary Method)

Build and run all services (bot, lavalink, postgres):
```bash
docker compose up -d
```

Rebuild after code changes:
```bash
docker-compose up --build -d
```

Helper scripts for rebuild with cleanup:
```bash
./scripts/rebuild-and-prune.sh      # Linux
.\scripts\rebuild-and-prune.ps1     # Windows
```

### Linting

PyLint is required and runs on all pushes via GitHub Actions:
```bash
find . -name '*.py' ! -path "./deprecated/*" | xargs pylint
```

Configuration in `.pylintrc` (Google Python style guide based)

### Documentation

Docusaurus site in `docs/`:
```bash
cd docs && npm install
npm start  # Preview at localhost:3000
```

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

Central error mapping in `libraries.py` maps exception types to user-friendly messages. `on_command_error` in bot.py handles all command errors.

### Database Connections

Database connection managed via psycopg2 connection pool with retry logic (5 attempts with exponential backoff). Queries class wraps all DB operations. Connection validated every 60s via `validate_db` task.

**Important**: The `main` service in docker-compose.yml uses `depends_on` with `service_healthy` condition to ensure PostgreSQL is fully ready before the bot starts. This prevents race conditions during container startup.

### Wavelink Integration

Lavalink node connects at startup in `connect_nodes()`. Node URI is `http://lavalink:2333` (Docker internal networking).

## Important Notes

- Bot requires all Discord intents (`Intents.all()`)
- Command prefix is `!` but bot primarily uses slash commands
- PATCHES_CHANNEL environment variable references a specific Discord channel for game update notifications
- Auto-channel creation tracks created channels in `created_channels` set to manage cleanup
- Patch notes are sent on startup if SEND_PATCH_NOTES=true
