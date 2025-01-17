import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from data.config import TOKEN
from db.connect import startup_table
from handlers.first_commands import mrouter
from middlewares import RateLimitMiddleware

dp = Dispatcher(storage=MemoryStorage())
dp.message.middleware(RateLimitMiddleware(user_limit_per_second=2, global_limit_per_second=30))


async def main() -> None:
    dp.startup.register(startup_table)
    dp.include_router(mrouter)

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
