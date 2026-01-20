- **Version 2.0.6** brings performance improvements and bug fixes for a smoother experience!

### What's New

- **Faster Command Responses** - Fixed performance bottlenecks that could cause delays
- **More Reliable Bug Reporting** - Improved `/reportbug` and `/featurerequest` commands to work more consistently
- **Better Startup Reliability** - Fixed issues that could prevent the bot from starting correctly
- **Improved Help Command** - `/help` command now loads faster and more reliably
- **Fixed Game Notifications** - Game update notifications now properly mention subscribed users

### Bug Fixes

- Fixed issue where bug reports and feature requests could fail to submit
- Fixed startup crash when configuration values were invalid or missing
- Resolved performance issues that could slow down the bot during heavy usage
- Fixed channel creation reliability when users switch channels([#152](https://github.com/aaron-rai/dollar-discord-bot/issues/152))
- Fixed game notification system not properly tagging subscribed users
- Fixed game notification system creating threads on every notification even when no users were subscribed([#150](https://github.com/aaron-rai/dollar-discord-bot/issues/150))
- Fixed crash when notifying users for games with no subscribers
