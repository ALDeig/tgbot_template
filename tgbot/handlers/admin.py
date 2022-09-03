from aiogram import Dispatcher
from aiogram.types import Message


async def admin_start(msg: Message):
    await msg.reply("Hello, admin!")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
