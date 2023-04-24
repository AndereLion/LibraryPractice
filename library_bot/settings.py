import os


class BotSettings:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DOTENV_PATH = os.path.join(BASE_DIR, ".env")

    if os.path.exists(DOTENV_PATH):
        from dotenv import load_dotenv
        load_dotenv(DOTENV_PATH)

    BOT_TOKEN = os.environ["BOT_TOKEN"]
    CHAT_ID = os.environ["CHAT_ID"]


settings = BotSettings()
