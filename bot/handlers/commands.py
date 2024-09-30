from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import ReplyKeyboardRemove

from bot.lexicon import LEXICON_COMMANDS
from bot.database import requests as rq
from bot.keyboards.inline_keyboards import (
    get_btns_category,
    get_btns_schemes,
    get_callback_btns,
)


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
async def cmd_exercises(message: Message, session: AsyncSession):
    data = await rq.get_all_category(session=session)
    await message.answer(text="List Exercises:", reply_markup=get_btns_category(data))


@router.callback_query(F.data.startswith("category:"))
async def get_schemes_by_category(callback: CallbackQuery, session: AsyncSession):
    cat_id = callback.data.lstrip("category:")
    data_schemes = await rq.get_all_scheme_on_category(session, int(cat_id))
    await callback.answer("ok")
    if data_schemes:
        await callback.message.edit_text(
            text="Список тренировочных схем:",
            reply_markup=get_btns_schemes(data_schemes),
        )
    else:
        await callback.message.edit_text(text="Scheme not found")


@router.callback_query(F.data.startswith("scheme:"))
async def show_scheme(callback: CallbackQuery, session: AsyncSession):
    scheme_id = callback.data.lstrip("scheme:")
    scheme = await rq.get_scheme_by_id(session, int(scheme_id))

    await callback.answer("ok")
    await callback.message.edit_text(
        text=f"Category: {scheme.category.title}\nTitle: {scheme.title}\nContent:\n{scheme.content}",
        reply_markup=get_callback_btns(
            btns={"Back": f"category:{scheme.category_id}"}, sizes=(1,)
        ),
    )


@router.message(Command("add_exercise"))
async def cmd_add_exercise(message: Message):
    await message.answer(text="This is command /add_exercise")


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
