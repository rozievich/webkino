from aiogram import types, Bot, Router
from aiogram.filters.command import CommandStart, Command

from data.config import ADMINS
from keyboards.inline_keyboards import forced_channel, rich_btn
from keyboards.reply_keyboards import admin_btn
from models.model import create_user, get_channel_order, get_join_request

mrouter = Router()


@mrouter.message(CommandStart())
async def welcome_handler(msg: types.Message, bot: Bot):
    await create_user(msg.from_user.id)
    check = await check_sub_channels(int(msg.from_user.id), bot)
    if check[0]:
        await bot.set_my_commands([types.BotCommand(command="start", description="Ishga tushirish ♻️")])
        await bot.send_message(msg.chat.id, text=f"Assalomu alaykum {msg.from_user.first_name} 🤖\n<b>Film Dunyosi Bot</b> - orqali siz o'zingizga yoqqan kinoni topishingiz mumkin 🎬\nMenga kino kodini yoki Instagram URL manzilini yuboring ✅", reply_markup=rich_btn())
    else:
        await msg.answer("Botdan foydalanish uchun ⚠️\nIltimos quidagi kanallarga obuna bo'ling ‼️", reply_markup=forced_channel(check[1]))


@mrouter.message(Command("panel"))
async def admin_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer(f"Assalomu alaykum {msg.from_user.first_name} 🤖\nAdmin sahifaga xush kelibsiz ⚙️", reply_markup=admin_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


async def check_sub_channels(user_id: int, bot: Bot):
    if user_id in ADMINS:
        return True, []
    else:
        channels = await get_channel_order(is_order=False)
        request_channels = await get_channel_order(is_order=True)
        unsubscribed_channels = []

        for channel in channels:
            chat_member = await bot.get_chat_member(chat_id=channel[2], user_id=user_id)
            if chat_member.status == "left":
                unsubscribed_channels.append(channel)

        if request_channels:
            summa = 0
            for channel in request_channels:
                info = await get_join_request(channel[2], str(user_id))
                if info:
                    summa += 1
                else:
                    unsubscribed_channels.append(channel)

            return summa == len(request_channels), unsubscribed_channels
        else:
            return len(unsubscribed_channels) == 0, unsubscribed_channels
