---
sidebar_position: 2
---

# Installation

Getting started with Dollar is quick and easy! Follow these steps to add Dollar to your Discord server and configure it for optimal performance.

## Step 1: Add Dollar to Your Server

Click the link below to authorize Dollar to join your Discord server:

**[Add Dollar to Discord](https://discord.com/api/oauth2/authorize?client_id=1044813990473257081&permissions=8&scope=applications.commands%20bot)**

You'll need to:
- Select the server where you want to add Dollar
- Agree to the permissions requested

## Step 2: Configure Dollar with /dollarsettings

Once Dollar has joined your server, you'll need to configure it using the `/dollarsettings` command. This command sets up the essential channels Dollar needs to operate:

1. **Text Channel**: The designated channel where users can enter bot commands
2. **Voice Channel**: A "JOIN HERE" channel for auto channel creation
3. **Shows Channel**: A channel for game update notifications and patch notes

### How to Use /dollarsettings

1. Type `/dollarsettings` in any text channel
2. Follow the prompts to select or create:
   - Your preferred command channel (text)
   - Your preferred voice channel for auto-creation
   - Your preferred channel for game notifications

### Important Notes

- **Command Channel Restriction**: Dollar will **only** respond to commands entered in the text channel you designate during setup. This keeps your other channels clean and organized.
- **Guild Owner Only**: Only the server owner can run the `/dollarsettings` command to ensure proper server configuration.

## Step 3: Auto Channel Creation (Optional)

Dollar includes an auto channel creation feature that automatically creates temporary voice channels when users join the designated "JOIN HERE" channel.

### How It Works

1. A user joins the voice channel you designated in `/dollarsettings`
2. Dollar automatically creates a new personal voice channel for that user
3. The user is moved to their new personal channel
4. When all users leave the personal channel, it's automatically deleted

### Disabling Auto Channel Creation

If you don't want to use the auto channel creation feature:

Simply **delete the voice channel** that was created during the `/dollarsettings` configuration. Dollar will detect that the channel no longer exists and won't attempt to create new channels.

## Step 4: Start Using Dollar!

That's it! Dollar is now ready to use. Here are some commands to get started:

- `/play <song>` - Play music in your voice channel
- `/help` - View all available commands
- `/reportbug` - Report any issues you encounter
- `/featurerequest` - Suggest new features

## Troubleshooting

### Dollar Isn't Responding to Commands

- Verify you're using commands in the designated text channel
- Ensure Dollar has the necessary permissions in that channel
- Try running `/dollarsettings` again to reconfigure
- Create an issue on the [GitHub repository](https://github.com/aaron-rai/dollar-discord-bot) if problems persist
  - Include details about your server setup and any error messages

### Auto Channels Aren't Being Created

- Verify the voice channel still exists
- Check that Dollar has permissions to create and manage channels
- Ensure users are joining the correct "JOIN HERE" voice channel

### Need More Help?

- Check out the [full documentation](https://aaron-rai.github.io/dollar-discord-bot/)
- Use `/reportbug` to report issues
- Visit the [GitHub repository](https://github.com/aaron-rai/dollar-discord-bot) for more information

---

Ready to explore Dollar's features? Check out the [Music Commands](3-Music/1-overview.md) section to learn about all the audio capabilities!
