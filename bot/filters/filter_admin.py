from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.config_data.config import settings


class IsAdmin(BaseFilter):
    def __init__(self) -> None:
        self.list_admin = [int(admin_id) for admin_id in settings.admin_list.split(",")]

    async def __call__(self, message: Message) -> Any:
        return message.from_user.id in self.list_admin
