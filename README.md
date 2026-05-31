# Mod-bot - Discord Moderation Bot

A comprehensive Discord moderation bot with all essential moderation commands.

## Features

✅ **Moderation Commands**
- Kick & Ban members
- Mute/Unmute members
- Warn members
- Purge/Clear messages
- Channel lock/unlock
- Timeout members (Discord's native timeout)
- Manage nicknames
- Slowmode control

✅ **Utility Commands**
- Ping (check bot latency)
- Server info
- User info
- Avatar display

## Installation

### Prerequisites
- Python 3.9 or higher
- Discord.py 2.3.2+

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/bhboru2-hub/Mod-bot.git
   cd Mod-bot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create Discord Bot Application**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application"
   - Go to "Bot" section and click "Add Bot"
   - Copy your bot token

5. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Paste your bot token in the `.env` file:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```

6. **Set bot permissions**
   - In Developer Portal, go to OAuth2 → URL Generator
   - Select scopes: `bot`
   - Select permissions:
     - Manage Messages
     - Manage Roles
     - Manage Channels
     - Kick Members
     - Ban Members
     - Moderate Members
   - Copy and use the generated URL to invite bot to your server

7. **Run the bot**
   ```bash
   python bot.py
   ```

## Commands

### Moderation Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `!kick` | `!kick @user [reason]` | Kick a member from the server |
| `!ban` | `!ban @user [reason]` | Ban a member from the server |
| `!unban` | `!unban user#0000 [reason]` | Unban a user |
| `!mute` | `!mute @user [duration] [reason]` | Mute a member |
| `!unmute` | `!unmute @user [reason]` | Unmute a member |
| `!warn` | `!warn @user [reason]` | Warn a member |
| `!timeout` | `!timeout @user <duration> [reason]` | Timeout a member (seconds) |
| `!untimeout` | `!untimeout @user [reason]` | Remove timeout from member |
| `!purge` | `!purge [amount]` | Delete messages (max 100) |
| `!clear` | `!clear [amount]` | Alias for purge |
| `!slowmode` | `!slowmode [seconds]` | Set channel slowmode |
| `!lock` | `!lock` | Lock the current channel |
| `!unlock` | `!unlock` | Unlock the current channel |
| `!nickname` | `!nickname @user [new_name]` | Change member nickname |
| `!modhelp` | `!modhelp` | Show all moderation commands |

### Utility Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `!ping` | `!ping` | Check bot latency |
| `!serverinfo` | `!serverinfo` | Get server information |
| `!userinfo` | `!userinfo [@user]` | Get user information |
| `!avatar` | `!avatar [@user]` | Display user avatar |

## Bot Structure

```
Mod-bot/
├── bot.py              # Main bot file
├── requirements.txt    # Python dependencies
├── .env.example       # Example environment file
├── README.md          # This file
└── cogs/
    ├── moderation.py  # All moderation commands
    └── utility.py     # Utility commands
```

## Permissions Required

Make sure your bot has these permissions:
- ✅ Send Messages
- ✅ Embed Links
- ✅ Manage Messages
- ✅ Manage Roles
- ✅ Manage Channels
- ✅ Kick Members
- ✅ Ban Members
- ✅ Moderate Members (for timeouts)

## Troubleshooting

### Bot doesn't respond to commands
- Check that bot has permission to send messages in the channel
- Verify bot token is correct in `.env`
- Ensure bot has required permissions in the server
- Check that command prefix is `!`

### Mute role not created
- The bot will automatically create a "Muted" role on first use
- Ensure bot has permission to create roles and manage channels

### Timeout command doesn't work
- This requires Discord's native timeout feature (server boost level 0+)
- Bot must have "Moderate Members" permission

## Support

For issues or suggestions, please open an issue on GitHub.

## License

MIT License - Feel free to use and modify!
