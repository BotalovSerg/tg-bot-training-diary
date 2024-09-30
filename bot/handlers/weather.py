from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove

from bot.keyboards.reply_kb import keyboard
from bot.meteo.api_meteo import get_weather


router = Router()


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
    data = get_weather(latitude, longitude)
    if data:
        await message.answer(
            text=f"Сейчас на улице {data['temp']} градусов.\n"
            f"По ошушениям {data['feels_lik']}градусов.\n",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.answer(
            text="Сервис барахлит, давай чуток позже",
            reply_markup=ReplyKeyboardRemove(),
        )
