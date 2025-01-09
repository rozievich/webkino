import time
import asyncio
from aiogram import BaseMiddleware
from aiogram.types import Message


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, user_limit_per_second: int, global_limit_per_second: int):
        super().__init__()
        self.user_limit_per_second = user_limit_per_second
        self.global_limit_per_second = global_limit_per_second
        self.user_last_request_time = {}
        self.global_requests = []

    async def __call__(self, handler, event: Message, data: dict):
        current_time = time.time()
        user_id = event.from_user.id

        # Har bir foydalanuvchi uchun xabar yuborish tezligini cheklash
        if user_id in self.user_last_request_time:
            user_elapsed_time = current_time - self.user_last_request_time[user_id]
            if user_elapsed_time < 1 / self.user_limit_per_second:
                await asyncio.sleep(1 / self.user_limit_per_second - user_elapsed_time)

        # Umumiy so'rovlar uchun cheklov
        self.global_requests = [t for t in self.global_requests if current_time - t < 1]
        if len(self.global_requests) >= self.global_limit_per_second:
            await asyncio.sleep(1 / self.global_limit_per_second)

        # So'rov vaqtlarini yangilash
        self.user_last_request_time[user_id] = time.time()
        self.global_requests.append(time.time())

        # Xabarni handlerga uzatish
        return await handler(event, data)
