# dollar-discord-bot
---

<p align="center">
    <img src="https://img.shields.io/badge/author-aaronrai-blue" alt="Author Badge">
    <img src="https://img.shields.io/badge/PyLint-Passing-brightgreen" alt="Pylint Status Badge">
    <img src="https://github.com/aaron-rai/dollar-discord-bot/actions/workflows/runner.yml/badge.svg " alt="CI Badge">
    <img src="https://img.shields.io/badge/license-MIT-red" alt="License Badge">
</p>

> [!IMPORTANT]
> Docusarus available at our github([Dollar Docs](https://aaron-rai.github.io/dollar-discord-bot/)).

Dollar: Your all-in-one Discord companion! Powered by Lavalink, Dollar not only lets you play music from popular websites, but goes above and beyond. Dollar acts as a versatile moderator, creating personal voice channels and enforcing proper command usage.

With Dollar, you'll enjoy a seamless music experience. It intelligently responds to commands entered in the designated text channel and plays music exclusively when users are in the same voice channel. No more juggling multiple music platforms!

Stay tuned for frequent updates and exciting new features as Dollar continually evolves. Add Dollar and unleash the true potential of your Discord server!

## Installation

**Quick Start:**
1. [Add Dollar to your Discord server](https://discord.com/api/oauth2/authorize?client_id=1044813990473257081&permissions=8&scope=applications.commands%20bot)
2. Run `/dollarsettings` to configure your command channel, voice channel, and notifications channel
3. Start using Dollar with `/play`, `/help`, and more!

**Note:** Dollar only responds to commands in your designated text channel. To disable auto channel creation, simply delete the voice channel created during setup.

For detailed installation instructions and troubleshooting, see the [Installation Guide](https://aaron-rai.github.io/dollar-discord-bot/docs/installation).

## Contributing

### Python Environment Setup
- To contribute to the project, you must first set up a Python environment with the required dependencies.
- To install the dependencies, run the following command:

```bash
cd scripts && pip install -r requirements.txt
```

### Docker Setup

- To run the bot in a docker container, you must first build the image using the following command:
```bash
docker build -t dollar .
```
- Once the image is built, you can run the container using the following command:
```bash
docker compose up -d
```
- This will run the bot, lavalink, and the database in separate containers. The bot will be connected to the database and lavalink automatically.
- After making code changes, you can rebuild the image and restart the container using the following commands:
```bash
docker-compose up --build -d
```

- A helper script has been created to make this process easier. To use the script, run the following command:

Windows:
```bash
.\scripts\rebuild-and-prune.ps1
```

Linux:
```bash
./scripts/rebuild-and-prune.sh
```

### .env.template

- The `.env.template` file contains the environment variables that the bot requires to run.
- To run the bot, you must create a `.env` file in the root directory and populate it with the required environment variables.

## Documentation Contribution Guidelines

- To contribute to the documentation, you must first install the Docusaurus package using the following command:
```bash
cd docs && npm install
```

- After making changes to the documentation, you can preview the changes using the following command:
```bash
npm start
```
