from decouple import config

DEBUG: bool = config("DEBUG", cast=bool, default=False)

TELEGRAM_CHAT_ID: str = config("TELEGRAM_CHAT_ID")
TELEGRAM_TOKEN: str = config("TELEGRAM_TOKEN")
