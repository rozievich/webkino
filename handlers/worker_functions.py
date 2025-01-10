import asyncio
from aiogram import types, Bot, F
from aiogram.fsm.context import FSMContext

from data.config import ADMINS
from keyboards.inline_keyboards import forced_channel, rich_btn
from keyboards.reply_keyboards import admin_btn, movies_btn, exit_btn, channels_btn, is_order_btn
from models.model import (statistika_movie, create_movie, get_channels, create_channel, delete_channel, \
                          get_movie, create_link, delete_link, check_order_channels, create_join_request, get_movies,
                          delete_movie_func, statistika_user, get_users)
from states.state_admin import AddMedia, AddChannelState, DeleteChannelState, ReklamaState, AddLinkState, \
    DeleteLinkState, DeleteMovieState
from .first_commands import check_sub_channels, mrouter
from utils.advertisement import send_advertisement


@mrouter.message(F.text == "Statistika 📊")
async def user_statistika_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer(text=await statistika_user(), reply_markup=admin_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mrouter.message(F.text == "Kinolar 🎬")
async def media_statistika_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer("Kinolar kategoriyasiga xush kelibsiz 🛠", reply_markup=movies_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mrouter.message(F.text == "Kino Statistika 📊")
async def kino_statistika_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer(text=await statistika_movie(), reply_markup=movies_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mrouter.message(F.text == "Kino qo'shish 📥")
async def kino_add_handler(msg: types.Message, state: FSMContext):
    if msg.from_user.id in ADMINS:
        await state.set_state(AddMedia.media)
        await msg.answer("Kinoni yuborishingiz mumkin 🎬", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mrouter.message(AddMedia.media)
async def handle_video(msg: types.Message, state: FSMContext):
    try:
        if msg.text == "❌":
            await msg.answer("Kino yuklash bekor qilindi ❌", reply_markup=movies_btn())
            await state.clear()
        else:
            print(msg)
            await state.update_data(file_id=msg.video.file_id, caption=msg.caption)
            await state.set_state(AddMedia.url)
            await msg.answer(text="Iltimos Kinoning Instagramdagi URL manzilini kiriting: ", reply_markup=exit_btn())
    except:
        await msg.answer("Iltimos Kino yuboring!", reply_markup=exit_btn())


@mrouter.message(AddMedia.url)
async def handle_media_url(msg: types.Message, state: FSMContext):
    try:
        if msg.text == "❌":
            await msg.answer("Kino yuklash bekor qilindi ❌", reply_markup=movies_btn())
            await state.clear()
        else:
            await state.update_data(url=msg.text)
            await state.set_state(AddMedia.media_id)
            await msg.answer(text="Iltimos Kino uchun ID kiriting: ", reply_markup=exit_btn())
    except Exception as e:
        await msg.answer("Iltimos to'g'ri URL manzilni yuboring!", reply_markup=exit_btn())


@mrouter.message(AddMedia.media_id)
async def handle_media_id(msg: types.Message, state: FSMContext):
    try:
        if msg.text == "❌":
            await msg.answer("Kino yuklash bekor qilindi ❌", reply_markup=movies_btn())
            await state.clear()
        elif not await get_movie(int(msg.text)):
            film_info = await state.get_data()
            data = await create_movie(file_id=film_info['file_id'], caption=film_info['caption'], post_id=int(msg.text),
                                      url=film_info['url'])
            if data:
                await msg.reply(f"Kino malumotlar bazasiga saqlandi ✅\nKino Kodi: {data}", reply_markup=movies_btn())
            await state.clear()
        else:
            await msg.reply(f"{msg.text} - ID bilan kino mavjud!")
    except Exception as e:
        print(e)
        await msg.answer("Iltimos Kod sifatida Raqam yuboring!", reply_markup=exit_btn())


@mrouter.message(F.text == "Kino o'chirish 🗑")
async def handle_delete_media_func(msg: types.Message, state: FSMContext):
    if msg.from_user.id in ADMINS:
        await state.set_state(DeleteMovieState.post_id)
        await msg.answer("Kinoni Kodini yuborishingiz mumkin 🎬", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mrouter.message(DeleteMovieState.post_id)
async def handle_delete_media(msg: types.Message, state: FSMContext):
    try:
        if msg.text == "❌":
            await msg.answer("Kino o'chirish bekor qilindi ❌", reply_markup=movies_btn())
            await state.clear()
        else:
            data = await delete_movie_func(int(msg.text))
            await msg.reply(text=data, reply_markup=movies_btn())
            await state.clear()
    except:
        await msg.answer("Iltimos Kod sifatida Raqam yuboring!", reply_markup=exit_btn())


@mrouter.message(F.text == "Kanallar 🖇")
async def channels_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer(text=await get_channels(), reply_markup=channels_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mrouter.message(F.text == "Kanal qo'shish ⚙️")
async def add_channel_handler(msg: types.Message, state: FSMContext):
    if msg.from_user.id in ADMINS:
        await state.set_state(AddChannelState.username)
        await msg.answer(text="Qo'shish kerak bo'lgan kanal linkini kiriting ✍️", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mrouter.message(AddChannelState.username)
async def add_channel_username_handler(msg: types.Message, state: FSMContext):
    try:
        if msg.text == "❌":
            await msg.answer("Kanal qo'shish bekor qilindi ❌", reply_markup=channels_btn())
            await state.clear()
        else:
            await state.update_data(username=msg.text)
            await state.set_state(AddChannelState.channel_id)
            await msg.answer(text="Iltimos Kanal ID kiriting: ", reply_markup=exit_btn())
    except:
        pass


@mrouter.message(AddChannelState.channel_id)
async def add_channel_handler_func(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await msg.answer("Kanal qo'shish bekor qilindi ❌", reply_markup=channels_btn())
        await state.clear()
    else:
        await state.update_data(channel_id=msg.text)
        await state.set_state(AddChannelState.is_order)
        await msg.answer(text="Bu kanal buyurtma kanalmi  ⁉️", reply_markup=is_order_btn())


@mrouter.message(AddChannelState.is_order)
async def is_order_handler(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await msg.answer("Kanal qo'shish bekor qilindi ❌", reply_markup=channels_btn())
        await state.clear()
    else:
        channel_info = await state.get_data()
        data = await create_channel(channel_info['username'], channel_info['channel_id'],
                                    True if msg.text == "Ha ✅" else False)
        if data:
            await msg.answer("Kanal muvaffaqiyatli qo'shildi ✅", reply_markup=channels_btn())
            await state.clear()
        else:
            await msg.answer("Bu kanal oldin qo'shilgan ❌", reply_markup=channels_btn())
            await state.clear()


@mrouter.message(F.text == "Kanal o'chirish 🗑")
async def movie_delete_handler(msg: types.Message, state: FSMContext):
    if msg.from_user.id in ADMINS:
        await state.set_state(DeleteChannelState.username)
        await msg.answer(text="O'chirish kerak bo'lgan kanal ID kiriting ✍️", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mrouter.message(DeleteChannelState.username)
async def delete_channel_handler_func(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await msg.answer("Kanal o'chirish bekor qilindi ❌", reply_markup=channels_btn())
        await state.clear()
    else:
        data = await delete_channel(msg.text)
        if data:
            await msg.answer("Kanal muvaffaqiyatli o'chirildi ✅", reply_markup=channels_btn())
        else:
            await msg.answer("Bunday ID uchun kanal mavjud emas ❌", reply_markup=channels_btn())
        await state.clear()


@mrouter.message(F.text == "Link qo'shish ⚙️")
async def add_channel_handler(msg: types.Message, state: FSMContext):
    if msg.from_user.id in ADMINS:
        await state.set_state(AddLinkState.link)
        await msg.answer(text="Qo'shish kerak bo'lgan Linkni kiriting ✍️", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mrouter.message(AddLinkState.link)
async def add_channel_handler_func(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await msg.answer("Link qo'shish bekor qilindi ❌", reply_markup=channels_btn())
        await state.clear()
    else:
        data = await create_link(url=msg.text)
        if data:
            await msg.answer("Link muvaffaqiyatli qo'shildi ✅", reply_markup=channels_btn())
            await state.clear()
        else:
            await msg.answer("Bu Link oldin qo'shilgan ❌", reply_markup=channels_btn())
            await state.clear()


@mrouter.message(F.text == "Link o'chirish 🗑")
async def movie_delete_handler(msg: types.Message, state: FSMContext):
    if msg.from_user.id in ADMINS:
        await state.set_state(DeleteLinkState.link)
        await msg.answer(text="O'chirish kerak bo'lgan Linkni kiriting ✍️", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mrouter.message(DeleteLinkState.link)
async def delete_channel_handler_func(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await msg.answer("Link o'chirish bekor qilindi ❌", reply_markup=channels_btn())
        await state.clear()
    else:
        data = await delete_link(msg.text)
        if data:
            await msg.answer("Link muvaffaqiyatli o'chirildi ✅", reply_markup=channels_btn())
        else:
            await msg.answer("Bunday Link mavjud emas ❌", reply_markup=channels_btn())
        await state.clear()


@mrouter.message(F.text == "Reklama 🎁")
async def reklama_handler(msg: types.Message, bot: Bot, state: FSMContext):
    if msg.from_user.id in ADMINS:
        await state.set_state(ReklamaState.rek)
        await bot.send_message(chat_id=msg.chat.id, text="Reklama tarqatish bo'limi 🤖", reply_markup=exit_btn())
    else:
        await bot.send_message(chat_id=msg.chat.id, text="Siz admin emassiz ❌",
                               reply_markup=types.ReplyKeyboardRemove())


@mrouter.message(ReklamaState.rek)
async def rek_state_handler(msg: types.Message, bot: Bot, state: FSMContext):
    if msg.text == "❌":
        await bot.send_message(chat_id=msg.chat.id, text="Reklama yuborish bekor qilindi 🤖❌", reply_markup=admin_btn())
        await state.clear()
    else:
        await bot.send_message(chat_id=msg.chat.id, text="Reklama yuborish boshlandi 🤖✅", reply_markup=admin_btn())
        await state.clear()

        all_users = await get_users()

        batch_size = 20
        success_count = 0

        for i in range(0, len(all_users), batch_size):
            batch = all_users[i:i + batch_size]
            batch_tasks = [send_advertisement(int(user['telegram_id']), msg, bot) for user in batch]
            results = await asyncio.gather(*batch_tasks)
            success_count += sum(results)
            await asyncio.sleep(1)

        failed_count = len(all_users) - success_count

        admin_tasks = [
            bot.send_message(
                chat_id=admin,
                text=f"Reklama yuborilgan foydalanuvchilar soni: {success_count}\n"
                     f"Botni bloklagan userlar soni: {failed_count}"
            )
            for admin in ADMINS
        ]

        await asyncio.gather(*admin_tasks)


@mrouter.callback_query(F.data == "channel_check")
async def channel_check_handler(callback: types.CallbackQuery, bot: Bot):
    check = await check_sub_channels(callback.from_user.id, bot)
    if check:
        await callback.message.delete()
        await callback.answer("Obuna bo'lganingiz uchun rahmat ☺️")
    else:
        await callback.message.answer("Botdan foydalanish uchun ⚠️\nIltimos quidagi kanallarga obuna bo'ling ‼️",
                                      reply_markup=forced_channel())


@mrouter.message(F.text == "❌")
async def exit_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer("Bosh menyu 🔮", reply_markup=admin_btn())


@mrouter.message(F.text)
async def forward_last_video(msg: types.Message, bot: Bot):
    check = await check_sub_channels(int(msg.from_user.id), bot)
    if check:
        data = await get_movie(int(msg.text) if msg.text.isdigit() else msg.text)
        all_movie = await get_movies()
        if data:
            try:
                await bot.send_video(chat_id=msg.from_user.id, video=data[0], caption=f"{data[1]}\n\n🤖 Bizning bot: @filimdunyosi_bot")
                await msg.answer(f"<b> 📥 Yuklangan: {len(all_movie)} ta</b>", reply_markup=rich_btn())
            except:
                await msg.reply(f"{msg.text} - id bilan hech qanday kino topilmadi ❌")
        else:
            await msg.reply(f"{msg.text} - id bilan hech qanday kino topilmadi ❌")
    else:
        await msg.answer("Botdan foydalanish uchun ⚠️\nIltimos quidagi kanallarga obuna bo'ling ‼️",
                         reply_markup=forced_channel())


@mrouter.chat_join_request()
async def chat_join_request_handler(chat_join_request: types.ChatJoinRequest):
    info = await check_order_channels(str(chat_join_request.chat.id))
    if info:
        await create_join_request(str(chat_join_request.chat.id), str(chat_join_request.from_user.id))
