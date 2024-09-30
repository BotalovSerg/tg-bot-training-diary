from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database import CategoryScheme, Scheme


def get_callback_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2,),
):
    keyboard = InlineKeyboardBuilder()
    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


def get_url_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2,),
):
    keyboard = InlineKeyboardBuilder()
    for text, url in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, url=url))

    return keyboard.adjust(*sizes).as_markup()


def get_btns_workout(data):
    keyboard = InlineKeyboardBuilder()

    for num, item in enumerate(data, start=1):
        time = item["time"].strftime("%d:%m:%y")
        train = item["train"]["description"]
        keyboard.row(
            InlineKeyboardButton(
                text=f"#{num}. Дата: {time} train - {train}",
                callback_data="workout:" + str(item["_id"]),
            )
        )

    return keyboard.as_markup()


def get_btns_category(data: list[CategoryScheme]):
    keyboard = InlineKeyboardBuilder()

    for num, item in enumerate(data, start=1):
        keyboard.row(
            InlineKeyboardButton(
                text=f"#{num}. {item.title}",
                callback_data="category:" + str(item.id),
            )
        )
    keyboard.row(InlineKeyboardButton(text="Cansel", callback_data="btn_cancel"))
    return keyboard.as_markup()


def get_btns_schemes(data: list[Scheme]):
    keyboard = InlineKeyboardBuilder()

    for num, item in enumerate(data, start=1):
        keyboard.row(
            InlineKeyboardButton(
                text=f"#{num}. {item.title}",
                callback_data="scheme:" + str(item.id),
            )
        )
    keyboard.row(InlineKeyboardButton(text="Cansel", callback_data="btn_cancel"))
    return keyboard.as_markup()
