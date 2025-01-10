import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMINS = [647857662, 5553781606]
ALL_FILM_CHANNEL = "https://t.me/toshkentzafarbekabod"
DB_NAME = "kino_db"
DB_PASSWORD = "black0613"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://f09a-90-156-163-151.ngrok-free.app{WEBHOOK_PATH}"
