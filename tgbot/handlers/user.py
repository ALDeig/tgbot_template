from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.db_queries import Db


async def user_start(msg: Message, db: Db):
    await msg.reply("Hello, user!")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
