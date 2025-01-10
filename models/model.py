from itertools import count

from .orm import Base, MediaClass, ChannelClass, LinkClass, JoinRequest

user = Base("users")
channel = ChannelClass("channels")
movie = MediaClass("movies")
links = LinkClass("links")
jrequst = JoinRequest("join_requests")


# User table data


async def create_user(telegram_id: int):
    data = user.get(telegram_id=str(telegram_id))
    if not data:
        user.create(telegram_id=str(telegram_id))
        return True
    else:
        return False


async def get_users():
    return user.get_all()


async def statistika_user():
    data = user.statistika()
    all_user = count(user.get_all())
    if data:
        return f"Userlar statistikasi 📊\n\nOxirgi 30 kunlik userlar: {len(data['month'])}\nOxirgi 7 kunlik userlar: {len(data['week'])}\nOxirgi 24 soatlik userlar: {len(data['day'])}\n\nBarcha Userlar soni: {all_user}"
    else:
        return False


# Movies table data
async def create_movie(file_id: str, caption: str, post_id: int, url: str) -> int:
    data = movie.get(file_id=file_id)
    if not data:
        movie.create_data(file_id=file_id, caption=caption, post_id=post_id, url=url)
        return post_id
    else:
        return data.get('post_id', None)


async def get_movie(post_id):
    column = "post_id" if isinstance(post_id, int) else "url" if isinstance(post_id, str) else None
    if column:
        data = movie.get(**{column: post_id})
        return [data['file_id'], data['caption']] if data else False
    return False


async def delete_movie_func(post_id: int):
    data = movie.get(post_id=post_id)
    if data:
        try:
            movie.delete_movie(post_id=post_id)
            return f"Kino muvaffaqiyatli o'chirildi ✅"
        except:
            return f"Kino o'chrishda xatolik yuzaga keldi ❌"
    else:
        return f"{post_id} - ID bilan kino topilmadi ❌"


async def get_movies():
    return movie.get_all()


async def statistika_movie():
    data = movie.statistika()
    all_data = movie.get_all()
    if data:
        return (f"Admin uchun Kinolar statistikasi 📊\n\n"
                f"Oxirgi 30 kun ichida yuklangan kinolar soni: {len(data['month'])}\n"
                f"Oxirgi 7 kun ichida yuklangan kinolar soni: {len(data['week'])}\n"
                f"Oxirgi 24 soat ichida yuklangan kinolar soni: {len(data['day'])}\n\n"
                f"Barcha Kinolar soni: {len(all_data)}")
    else:
        return False


# Channel table data
async def create_channel(username: str, channel_id: str, is_order: bool):
    data = channel.get(channel_id=channel_id)
    if data:
        return False
    else:
        channel.create_data(username=username, channel_id=channel_id, is_order=is_order)
        return True


async def delete_channel(channel_id: str):
    data = channel.get(channel_id=channel_id)
    if data:
        channel.delete_data(channel_id=channel_id)
        return True
    else:
        return None


async def get_channels():
    data = channel.get_all()
    links_info = links.get_all()
    text = f"Hamkor Kanallar ro'yhati 📥\n\n"
    for i in data:
        text += f"{i['username']}\n"
    else:
        text += "\nHamkor Linklar ro'yhati 🔗\n\n"
        for j in links_info:
            text += f"{j['link']}\n"
    return text


async def get_channel_order(is_order: bool):
    return channel.get_all(is_order=is_order)


# Links table data
async def create_link(url: str):
    data = links.get(link=url)
    if data:
        return False
    else:
        links.create_data(link=url)
        return True


async def delete_link(url: str):
    data = links.get(link=url)
    if data:
        links.delete(link=url)
        return True
    else:
        return None


async def check_order_channels(channel_id: str):
    data = channel.get(channel_id=channel_id)
    if data:
        return True
    else:
        return False


async def create_join_request(channel_id: str, user_id: str):
    data = jrequst.get(channel_id=channel_id, user_id=user_id)
    if data:
        return True
    else:
        jrequst.create_data(channel_id=channel_id, user_id=user_id)
        return True


async def get_join_request(channel_id: str, user_id: str):
    data = jrequst.get(channel_id=channel_id, user_id=user_id)
    if data:
        return data
    else:
        return None
