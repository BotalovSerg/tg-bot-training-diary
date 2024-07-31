from datetime import datetime
from bson.objectid import ObjectId

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from pymongo.collection import Collection

from bot.states.states import AddWorkoutSG
from bot.keyboards.inline_keyboards import get_callback_btns, get_btns_workout
from bot.database.mongodb import insert_workout


router = Router()


@router.message(StateFilter(None), Command("add_workout"))
async def cmd_add_workout(message: Message, state: FSMContext):
    await state.set_state(AddWorkoutSG.description)
    await message.answer(
        "Режим добавления тренировки.\nДобавь место и описание тренировки (кардио, силовая, бег, турники и т.д.)"
    )


@router.message(AddWorkoutSG.description, F.text)
async def set_date_workout(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddWorkoutSG.sheme)
    await message.answer(text="Запишите план тернировки, пункты, подходы")


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
    await callback.answer("OK")
    await callback.message.edit_text("Тренировка сохранена")

    insert_workout(collection_mongo, callback.from_user.id, data)


@router.message(Command("all_workout"))
async def get_all_workout_user(message: Message, collection_mongo: Collection):
    query = {"telegram_id": message.from_user.id}
    all_workout = collection_mongo.find(query, {"_id": 1, "time": 1, "train": 1}).sort(
        "time", -1
    )
    # for i in all_workout:
    #     print("i", i["_id"])
    #     dt: datetime = i["time"]
    #     print(dt.strftime("%d:%m:%y"))  # 30:07:24
    #     print(dt.strftime("%A, %d, %B, %Y, %H:%M"))  # Tuesday, 30, July, 2024, 19:42
    #     print("---------------")
    #     print(i["train"])
    #     print("---------------")
    #     print("---------------")

    await message.answer(text="all_workout", reply_markup=get_btns_workout(all_workout))
    # {'description': 'Турники, дома', 'sheme': '1. Подтягивание 5х5\n2. Отжимание 5х10'}
    # {'description': 'Беговая', 'sheme': '2 км\nРястяжка\nЗаминка'}
    # {'description': 'Йога 🧘\u200d♀️', 'sheme': 'То пятое десятое'}

    # i {'_id': ObjectId('66a8f63ca294b88ded429c33'),
    #  'time': datetime.datetime(2024, 7, 30, 19, 18, 36, 683000),
    # 'train': {'description': 'Турники, дома', 'sheme': '1. Подтягивание 5х5\n2. Отжимание 5х10'}}


@router.callback_query(F.data.startswith("workout:"))
async def get_workout_by_id(callback: CallbackQuery, collection_mongo: Collection):
    _id = callback.data.lstrip("workout:")
    res = collection_mongo.find_one({"_id": ObjectId(_id)}, {"_id": 0, "time": 1, "train": 1})

    print(res)

    time = res["time"].strftime("%A, %d, %B, %Y, %H:%M")
    desc = res["train"]["description"]
    sheme = res["train"]["sheme"]

    await callback.answer("res")
    await callback.message.edit_text(
        text=f"Тренировкаю Дата:{time}\nОписание:{desc}\nSheme:{sheme}"
    )