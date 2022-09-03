import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiogram.types import BotCommand, BotCommandScopeChat
from aiogram.utils.exceptions import ChatNotFound

from tgbot.config import get_settings 
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.user import register_user
from tgbot.middlewares.db import DbMiddleware
from tgbot.services.db_connection import get_session_factory
from tgbot.services.db_queries import Db
from tgbot.services.logger import setup_logger


def register_all_middlewares(dp):
    dp.setup_middleware(DbMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)


async def set_commands(dp: Dispatcher, admin_ids: list[int]):
    await dp.bot.set_my_commands(
        commands=[BotCommand("start", "Старт")]
    )
    commands_for_admin = [
        BotCommand("start", "Старт"),
    ]
    for admin_id in admin_ids:
        try:
            await dp.bot.set_my_commands(
                commands=commands_for_admin,
                scope=BotCommandScopeChat(admin_id)
            )
        except ChatNotFound as er:
            logging.error(f"Установка команд для администратора {admin_id}: {er}")


async def main():
    setup_logger("INFO")
    logging.info("Starting bot")
    config = get_settings()

    if config.tg.use_redis:
        storage = RedisStorage()
    else:
        storage = MemoryStorage()

    bot = Bot(token=config.tg.token, parse_mode="HTML")
    dp = Dispatcher(bot, storage=storage)

    bot["config"] = config
    db = Db(get_session_factory(config.db_url))
    await db.async_init()
    bot["db"] = db

    bot_info = await bot.get_me()
    logging.info(f'<yellow>Name: <b>{bot_info["first_name"]}</b>, username: {bot_info["username"]}</yellow>')

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)
    await set_commands(dp, config.tg.admins)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        # await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
