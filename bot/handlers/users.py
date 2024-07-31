from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession


from bot.keyboards.inline_keyboards import get_callback_btns
from bot.states.states import UpdateProfileSG
from bot.database import requests as rq


router = Router()


@router.message(Command("profile"))
async def cmd_profile(message: Message, session: AsyncSession):
    user = await rq.get_user_by_id(session=session, user_id=message.from_user.id)
    text = (
        f"👤\t<b>Profile</b>"
        "\n----------------------\n"
        f"<b>Username</b>: {user.username}\n"
        f"<b>ID</b>: {user.telegram_id or '-'}\n"
        f"<b>First name</b>: {user.first_name or '-'}\n"
        f"<b>Last name</b>: {user.last_name or '-'}\n"
        f"<b>Age</b>: {user.age or '-'}\n"
        f"<b>BIO</b>: {user.bio or '-'}\n"
    )
    await message.answer(
        text=text,
        reply_markup=get_callback_btns(
            btns={
                "Update": "update_profile",
                "Cansel": "cansel",
                "Back home": "back_home",
            }
        ),
    )


@router.callback_query(StateFilter(None), F.data == "update_profile")
async def update_profile_user(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UpdateProfileSG.first_name)
    await callback.answer("Режим обнавления профиля")
    await callback.message.edit_text("Введите ваше имя")


@router.message(UpdateProfileSG.first_name, F.text)
async def fsm_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(UpdateProfileSG.last_name)

    await message.answer("Напиши свою фамилию")


@router.message(UpdateProfileSG.last_name, F.text)
async def fsm_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(UpdateProfileSG.age)

    await message.answer("Введите ваш возраст")


@router.message(UpdateProfileSG.age, F.text)
async def fsm_last_name(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(UpdateProfileSG.bio)

    await message.answer("Напиши немного о себе")


@router.message(UpdateProfileSG.bio, F.text)
async def fsm_last_name(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(bio=message.text)
    data = await state.get_data()
    await state.clear()
    user_id = message.from_user.id
    await rq.update_profile_user(session=session, user_id=user_id, data=data)

    user = await rq.get_user_by_id(session=session, user_id=user_id)

    text = (
        f"👤\t<b>Profile</b>"
        "\n----------------------\n"
        f"<b>Username</b>: {user.username}\n"
        f"<b>ID</b>: {user.telegram_id or '-'}\n"
        f"<b>First name</b>: {user.first_name or '-'}\n"
        f"<b>Last name</b>: {user.last_name or '-'}\n"
        f"<b>Age</b>: {user.age or '-'}\n"
        f"<b>BIO</b>: {user.bio or '-'}\n"
    )
    await message.answer(
        text=text,
        reply_markup=get_callback_btns(
            btns={
                "Update": "update_profile",
                "Cansel": "cansel",
                "Back home": "back_home",
            }
        ),
    )
