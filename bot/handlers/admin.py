from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from bot.filters.filter_admin import IsAdmin

router = Router()
router.message.filter(IsAdmin())


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    await message.answer(text=f"This is admin{message.from_user.id}")
