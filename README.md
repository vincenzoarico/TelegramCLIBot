# TelegramCLIBot

![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Python](https://img.shields.io/badge/PYTHON-%20%203.14+-blue?style=for-the-badge)

TelegramCLIBot is a personal Telegram bot designed to execute shell commands directly from your mobile or desktop device via the Telegram app. It works as a remote CLI interface, allowing you to add custom commands, list them, delete them, and execute them on the server where the bot is running.

**Important note**: This bot is intended **exclusively for personal use**. It is not designed for public deployments. It allows execution of arbitrary shell commands, which makes it potentially dangerous if not used with caution. It is ideal for personal automation on a private server (e.g., Raspberry Pi or VPS in LAN).

## Warnings and Security Risks

**WARNING: HIGH RISKS!**

- **Arbitrary command execution**: The bot allows execution of any shell command via `/run` or custom commands. This includes potentially destructive commands (e.g., `rm -rf /`, `shutdown`, or access to sensitive files).
  
- **Personal use only**: Authentication is based on a list of authorized Telegram user IDs present in the configuration file. If the authorized Telegram account is compromised, an attacker could execute remote commands. Always use 2FA on your Telegram account.

- **No sandboxing**: Commands are executed directly on the host server.

## Requirements

- Python 3.14 or higher
- Telegram account (enable 2FA for security reasons)
- Server to run the bot (e.g., Linux, with a non-root user to mitigate damage)
- Poetry

## Installation

### Step 1: Create the Bot on Telegram with BotFather

1. Open Telegram and search for `@BotFather`.
2. Send `/newbot` and follow the instructions:
   - Assign a name to the bot (e.g., "MyPersonalCLIBot").
   - Assign a unique username (e.g., "my_personal_cli_bot").
3. BotFather will provide you with an **API Token** (e.g., `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`). Copy it and keep it secret.

### Step 2: Clone the Repository

Clone this repository from GitHub:

```bash
git clone https://github.com/vincenzoarico/telegramclibot.git
cd telegramclibot
poetry install
```

### Step 3: Configuration

Insert the bot token and Telegram user ID (to find it, send a message to the bot @myidbot) in the `config/config.yml` file.

**Configuration Example (`config/config.yml`):**

```yaml
telegram_api_token: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
allowed_user_ids:
  - 123456789
  - 987654321
```

Replace the token with your actual bot token from BotFather, and add your Telegram user ID(s) to the `allowed_user_ids` list.

## Running the Bot (Server-side)

```bash
cd telegramclibot
source $(poetry env info --path)/bin/activate
telegramclibot
```

Now, you can use the `telegramclibot` command from any path in your terminal.

**Note**: The command to deactivate the virtual environment created by Poetry is `deactivate`.

## Bot Commands

- `/start`: Welcome message
- `/run <shell_command>`: Execute an arbitrary shell command (e.g., `/run ls -l`)
- `/addcmd <name> <description> | <shell_command>`: Add a custom command (e.g., `/addcmd gitpull Git pull repo | git pull origin main`)
- `/delcmd <name>`: Delete a custom command
- `/listcmds`: List custom commands
- Custom commands: Send `/command_name` to execute it

The bot menu automatically updates with custom commands.

**Example**: After adding `/gitpull`, send `/gitpull` to execute `git pull origin main`.

Long outputs are chunked into multiple messages due to Telegram limits.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.
