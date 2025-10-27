import logging

from . import bot

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        format="[{asctime}] {levelname} {name}: {message}",
        style="{",
        datefmt="%d/%m/%Y %H:%M:%S",
        level=logging.INFO,  # 1. DEBUG (NO) 2. INFO (YES) 3. WARNING (YES) 4. ERROR (YES) 5. CRITICAL (YES)
    )
    logger.info("Starting...")

    if bot.bot_configuration():
        bot.bot_start()


if __name__ == "__main__":
    main()
