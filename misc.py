from aiogram.types import Update
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

from loader import bot, dp
from data.config import WEBHOOK_URL, WEBHOOK_PATH
from handlers.first_commands import mrouter
from db.connect import startup_table

@asynccontextmanager
async def lifespan(app: FastAPI):
    startup_table()
    await bot.set_webhook(WEBHOOK_URL)
    dp.include_routers(mrouter)
    print(f"Webhook set up: {WEBHOOK_URL}")
    yield
    await bot.delete_webhook()
    await bot.session.close()
    print("Webhook removed and bot session closed!")

app = FastAPI(lifespan=lifespan)

@app.post(WEBHOOK_PATH)
async def webhook_path_handler(request: Request):
    json_data = await request.json()
    update = Update(**json_data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}

@app.get("/connect")
async def test_connect_handler():
    return {"status": "ok", "message": "Connected successfully!"}
