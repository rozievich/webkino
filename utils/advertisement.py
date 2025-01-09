from aiogram import types


async def send_advertisement(user_id: int, message: types.Message, bot):
    try:
        await bot.copy_message(chat_id=int(user_id), from_chat_id=message.chat.id, message_id=message.message_id, caption=message.caption, caption_entities=message.caption_entities, reply_markup=message.reply_markup)
        return True
    except Exception as e:
        return False
