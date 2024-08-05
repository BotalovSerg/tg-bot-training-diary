import asyncio
import logging
from pymongo import MongoClient

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.config_data.config import settings
from bot.middlewares import DataBaseSession, MongoDBConnect
from bot.handlers import get_routers
from bot.keyboards.set_menu import set_main_menu
from bot.database.requests import test_connection


async def main():
    logger = logging.getLogger(__name__)
    engine = create_async_engine(url=str(settings.db.url), echo=settings.db.echo)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    mongo_client = MongoClient(settings.mongo_db.url, settings.mongo_db.port)

    async with session_maker() as session:
        await test_connection(session)
        logger.info("Connect db")

    bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    dp.update.middleware(MongoDBConnect(client=mongo_client))

    dp.include_routers(*get_routers())

    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
