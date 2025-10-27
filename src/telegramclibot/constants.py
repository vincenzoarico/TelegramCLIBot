from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "config.yml"
COMMANDS_FILE = PROJECT_ROOT / "data" / "commands.json"
