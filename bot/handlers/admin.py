from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.filter_admin import IsAdmin
from bot.keyboards.inline_keyboards import get_callback_btns
from bot.states.states import AddCategory
from bot.database.requests import create_category

router = Router()
router.message.filter(IsAdmin())


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    await message.answer(
        text=f"This is admin {message.from_user.id}.",
        reply_markup=get_callback_btns(
            btns={
                "create_category": "create_cat",
                "command_1": "cmd_1",
            },
            sizes=(1,),
        ),
    )


@router.callback_query(F.data == "create_cat")
async def cmd_create_cat(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddCategory.title)
    await callback.answer("Режим добавления категории")
    await callback.message.edit_text(text="Введите названия категории")


@router.message(AddCategory.title, F.text)
async def save_title_category(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    await create_category(session=session, title=message.text)
    await state.clear()
    await message.answer(text=f"Категория {message.text!r} сохранена.")
