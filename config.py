import os


class Config:
    SECRET_KEY = os.environ.get("FORM_SECRET")
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
    CHAT_ID = os.environ.get("CHAT_ID")
