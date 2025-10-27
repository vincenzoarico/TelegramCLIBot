import json
import logging
import subprocess
import shlex

from . import constants, globals

logger = logging.getLogger(__name__)


def execute_shell_command(command: str) -> str:
    logger.info(f"Command execution: {command}")

    try:
        args = shlex.split(command) 
    except ValueError as e:
        return f"❌ Error parsing command: {e}"

    try:
        process = subprocess.run(
            args,
            check=False,
            shell=False,
            capture_output=True,
            text=True,
            timeout=60,
            stderr=subprocess.STDOUT,
        )
        return process.stdout or "✅ Command successfully executed!"
    except Exception as e:
        return f"❌ Error during execution: {e}"


def load_commands_from_file():
    try:
        with constants.COMMANDS_FILE.open() as json_commands_file:
            content_json_commands_file = json_commands_file.read()
            if content_json_commands_file:
                globals.custom_commands = json.loads(content_json_commands_file)
                logger.info(
                    f"Commands loaded from the json file: {constants.COMMANDS_FILE}"
                )
    except (FileNotFoundError, json.JSONDecodeError):
        logger.warning("Commands file not found. Starting without the custom commands.")


def save_commands_to_file():
    try:
        with constants.COMMANDS_FILE.open("w") as json_commands_file:
            json.dump(globals.custom_commands, json_commands_file, indent=2)
            logger.info(f"Commands saved to the json file: {constants.COMMANDS_FILE}")
    except Exception:
        logger.exception("Impossible to save the commands.")
