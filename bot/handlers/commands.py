from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from bot.lexicon import LEXICON_COMMANDS
from bot.database import requests as rq


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    await rq.create_user(
        session=session,
        user_id=message.from_user.id,
        username=message.from_user.username,
    )
    await message.answer(text=LEXICON_COMMANDS["commands"][message.text])


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(text=LEXICON_COMMANDS["commands"][message.text])


@router.message(Command("exercises"))
async def cmd_exercises(message: Message):
    await message.answer(text="List Exercises")


@router.message(Command("add_exercise"))
async def cmd_add_exercise(message: Message):
    await message.answer(text="This is command /add_exercise")
