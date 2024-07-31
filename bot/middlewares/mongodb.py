from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from pymongo import MongoClient

from bot.config_data.config import settings


class MongoDBConnect(BaseMiddleware):
    def __init__(self, client: MongoClient):
        super().__init__()
        self.client = client

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        db = self.client[settings.mongo_db.NAME_DB]
        coll = db[settings.mongo_db.NAME_COLLECTION]
        data["collection_mongo"] = coll
        return await handler(event, data)
