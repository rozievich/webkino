import logging
import uvicorn
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from data.config import TOKEN
from middlewares import RateLimitMiddleware

dp = Dispatcher(storage=MemoryStorage())
dp.message.middleware(RateLimitMiddleware(user_limit_per_second=2, global_limit_per_second=30))
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    uvicorn.run(
        "misc:app",
        host="127.0.0.1",
        port=8443,
        reload=True
    )
