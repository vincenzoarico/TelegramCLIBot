import logging
import time

import yaml
from telebot import TeleBot, types

from . import commands, constants, globals

logger = logging.getLogger(__name__)

bot = None

BOT_TOKEN = ""
ALLOWED_USER_IDS = []


def bot_configuration() -> bool:
    global BOT_TOKEN, ALLOWED_USER_IDS, bot

    logger.info(f"Configuration started from the yaml file: {constants.CONFIG_FILE}")

    try:
        with constants.CONFIG_FILE.open() as yaml_config_file:
            config = yaml.safe_load(yaml_config_file)
            if config:
                BOT_TOKEN = config.get("telegram_api_token")
                ALLOWED_USER_IDS = config.get("allowed_user_ids")
                if (
                    BOT_TOKEN
                    and ALLOWED_USER_IDS
                    and type(BOT_TOKEN) is str
                    and BOT_TOKEN != "YOUR_BOT_TOKEN_API"
                    and (
                        isinstance(ALLOWED_USER_IDS, list)
                        and all(isinstance(id, int) for id in ALLOWED_USER_IDS)
                    )
                ):
                    bot = TeleBot(BOT_TOKEN)
                    setup_handlers()
                    commands.load_commands_from_file()
                    logger.info("Configuration loaded.")
                    return True
            logger.error("Configuration file not compiled correctly.")
            return False
    except FileNotFoundError:
        logger.exception("Configuration file not found.")
        return False


def update_bot_menu():
    if not bot:
        logger.error("Bot not initialized")
        return

    static_commands = [
        types.BotCommand("start", "Show welcome message"),
        types.BotCommand("run", "Execute shell command (/run <shell_command>)"),
        types.BotCommand("addcmd", "Add a custom command (/addcmd <command_name> <description> | <shell_command>)"),
        types.BotCommand("delcmd", "Delete a custom command (/delcmd <command_name>)"),
        types.BotCommand("listcmds", "Show all custom commands"),
    ]
    dynamic_commands = [
        types.BotCommand(name, data["description"])
        for name, data in globals.custom_commands.items()
    ]

    bot.set_my_commands(static_commands + dynamic_commands)

def bot_start():
    if not bot:
        logger.error("Bot not initialized")
        return

    logger.info("TelegramCLIBot started.")

    update_bot_menu()
    bot.infinity_polling(
        timeout=100,
        long_polling_timeout=90,
        skip_pending=True,
        allowed_updates=["message"],
    )


def is_user_allowed(message: types.Message) -> bool:
    if not bot:
        logger.error("Bot not initialized")
        return False

    if message.from_user.id not in ALLOWED_USER_IDS:
        bot.reply_to(message, " ❌ You are not authorized to use this bot.")
        return False
    return True


#################################### HANDLERS ####################################

def setup_handlers():

    @bot.message_handler(commands=["start"])
    def start_handler(message: types.Message):
        if not is_user_allowed(message):
            return
        bot.reply_to(message, "Welcome, I'm TelegramCLIBot!")


    @bot.message_handler(commands=["addcmd"])
    def add_command_helper(message: types.Message):
        if not is_user_allowed(message):
            return

        try:
            _, command_name, command_info = message.text.split(" ", 2)
            command_description, command_str = command_info.split("|", 1)
            command_name = command_name.strip().lower()
            command_description = command_description.strip()
            command_str = command_str.strip()
            if (
                command_name.isalnum()
                and command_name[0].isalpha()
                and len(command_name) <= 32
            ):
                globals.custom_commands[command_name] = {
                    "description": command_description,
                    "command": command_str,
                }
                commands.save_commands_to_file()
                update_bot_menu()
                bot.reply_to(
                    message, f"✅ Command `/{command_name}` added!", parse_mode="Markdown"
                )
            else:
                bot.reply_to(
                    message,
                    "❌ The command name can contain only letters and numbers, and the first character must be a letter.",
                )
        except ValueError:
            bot.reply_to(
                message,
                "❌ Incorrect syntax.\nUse: `/addcmd <name> <description> | <shell_command>`",
                parse_mode="Markdown",
            )


    @bot.message_handler(commands=["delcmd"])
    def delete_command_handler(message: types.Message):
        if not is_user_allowed(message):
            return

        try:
            command_name = message.text.split(" ", 1)[1].lower()
            if command_name in globals.custom_commands:
                del globals.custom_commands[command_name]
                commands.save_commands_to_file()
                update_bot_menu()
                bot.reply_to(message, f"✅ Command `/{command_name}` deleted.")
            else:
                bot.reply_to(message, f"❌ Command `/{command_name}` not found.")

        except IndexError:
            bot.reply_to(
                message,
                "❌ Incorrect syntax.\nUse: `/delcmd <name>`",
                parse_mode="Markdown",
            )


    @bot.message_handler(commands=["listcmds"])
    def list_commands_handler(message: types.Message):
        if not is_user_allowed(message):
            return

        if not globals.custom_commands:
            bot.reply_to(message, "No custom commands.")
            return

        response = "*Commands list:*\n\n" + "\n".join(
            [
                f"`/{name}`: {data['description']}"
                for name, data in globals.custom_commands.items()
            ]
        )
        bot.reply_to(message, response, parse_mode="Markdown")


    @bot.message_handler(commands=["run"])
    def run_handler(message: types.Message):
        if not is_user_allowed(message):
            return

        try:
            command_str = message.text.split(" ", 1)[1]
            command_output = commands.execute_shell_command(command_str)
            for i in range(0, len(command_output), 4096):
                bot.reply_to(
                    message, f"<pre>{command_output[i : i + 4096]}</pre>", parse_mode="HTML"
                )
                time.sleep(0.5)

        except IndexError:
            bot.reply_to(
                message,
                "❌ Incorrect syntax.\nUse: `/run <shell_command>`",
                parse_mode="Markdown",
            )


    @bot.message_handler(func=lambda message: message.text and message.text.startswith("/"))
    def dynamic_command_handler(message: types.Message):
        if not is_user_allowed(message):
            return

        command_name = message.text.lstrip("/")
        if command_name in globals.custom_commands:
            command_output = commands.execute_shell_command(
                globals.custom_commands[command_name]["command"]
            )
            for i in range(0, len(command_output), 4096):
                bot.reply_to(
                    message, f"<pre>{command_output[i : i + 4096]}</pre>", parse_mode="HTML"
                )
                time.sleep(0.5)
