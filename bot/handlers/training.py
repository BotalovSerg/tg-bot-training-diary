from datetime import datetime
from bson.objectid import ObjectId

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from pymongo.collection import Collection

from bot.states.states import AddWorkoutSG
from bot.keyboards.inline_keyboards import get_callback_btns, get_btns_workout
from bot.database.mongodb import insert_workout, get_all_workout
from bot.lexicon import LEXICON_MESSAGE

router = Router()


@router.message(default_state, Command("add_workout"))
async def cmd_add_workout(message: Message, state: FSMContext):
    await state.set_state(AddWorkoutSG.description)
    await message.answer(text=LEXICON_MESSAGE["text"]["add_workout"])


@router.message(AddWorkoutSG.description, F.text)
async def set_date_workout(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddWorkoutSG.sheme)
    await message.answer(text=LEXICON_MESSAGE["text"]["save_training_plan"])


@router.message(AddWorkoutSG.sheme, F.text)
async def set_descroption_workout(message: Message, state: FSMContext):
    await state.update_data(sheme=message.text)
    data = await state.get_data()
    await state.set_state(AddWorkoutSG.check)
    await message.answer(
        text=f"Посмотри перед сохранением\nDescroption: \n{data['description']}\nSheme: \n{data['sheme']}",
        reply_markup=get_callback_btns(btns={"Save": "save", "Cansel": "cancel"}),
    )


@router.callback_query(AddWorkoutSG.check, F.data == "save")
async def save_workout(
    callback: CallbackQuery,
    state: FSMContext,
    collection_mongo: Collection,
):
    data = await state.get_data()
    await state.clear()

    insert_workout(collection_mongo, callback.from_user.id, data)

    await callback.answer("OK")
    await callback.message.edit_text("Тренировка сохранена")


@router.message(Command("all_workout"))
async def get_all_workout_user(message: Message, collection_mongo: Collection):

    all_workout = get_all_workout(collection_mongo, message.from_user.id)

    await message.answer(text="all_workout", reply_markup=get_btns_workout(all_workout))


@router.callback_query(F.data.startswith("workout:"))
async def get_workout_by_id(callback: CallbackQuery, collection_mongo: Collection):
    _id = callback.data.lstrip("workout:")
    res = collection_mongo.find_one(
        {"_id": ObjectId(_id)}, {"_id": 0, "time": 1, "train": 1}
    )

    print(res)

    time = res["time"].strftime("%A, %d, %B, %Y, %H:%M")
    desc = res["train"]["description"]
    sheme = res["train"]["sheme"]

    await callback.answer("res")
    await callback.message.edit_text(
        text=f"Тренировкаю Дата:{time}\nОписание:{desc}\nSheme:{sheme}"
    )
