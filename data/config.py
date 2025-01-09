import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMINS = [647857662, 5553781606]
ALL_FILM_CHANNEL = "https://t.me/+zO18G6ZLkBc0ZDdi"
DB_NAME = "kino_db"
DB_PASSWORD = "black0613"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://e2cd-84-54-84-188.ngrok-free.app{WEBHOOK_PATH}"
