from aiogram.fsm.state import State, StatesGroup


class UpdateProfileSG(StatesGroup):
    first_name = State()
    last_name = State()
    age = State()
    bio = State()


class AddWorkoutSG(StatesGroup):
    description = State()
    sheme = State()
    check = State()


class AddCategory(StatesGroup):
    title = State()
