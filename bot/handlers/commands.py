from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import Command, CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import ReplyKeyboardRemove

from bot.lexicon import LEXICON_COMMANDS
from bot.database import requests as rq
from bot.keyboards.reply_kb import keyboard
from bot.meteo.api_meteo import get_weather


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


@router.message(Command("weather"))
async def cmd_weather(message: Message):
    await message.answer(
        text="Что бы узнать погоду, нужно поделиться геолокацией",
        reply_markup=keyboard,
    )

@router.message(F.content_type.in_("location"))
async def locations(message: Message):
    latitude = float(message.location.latitude)
    longitude = float(message.location.longitude)
    get_weather(latitude, longitude)
    await message.answer(
        text=f"Your location latitude = {message.location.latitude}\n"
             f"longitude = {message.location.longitude}",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(Command("cansel"), any_state)
async def cmd_cansel(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.reply(
            text="OK, но мы сейчас не находимся ни в каком состоянии.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return
    await state.clear()
    await message.answer(
        text=f"OK, начнем все с начала.",
        reply_markup=ReplyKeyboardRemove(),
    )
