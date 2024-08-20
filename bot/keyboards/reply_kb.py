from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard(
    *btns: str,
    placeholder: str = None,
    request_contact: int = None,
    request_location: int = None,
    sizes: tuple[int] = (2,),
):
    """
    Parametrs request_contact and request_location must be as indexes of btns args for buttons you need.
    Example:
    get_keyboard(
        "Menu",
        "About shop",
        "Name btn1",
        "Name btn2",
        placeholder="Who is it?",
        request_contact=4,
        sizes= (2, 2, 1),
    )
    """
    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder=placeholder
    )

kb_builder = ReplyKeyboardBuilder()

geo_btn = KeyboardButton(
    text='Отправить геолокацию',
    request_location=True
)

kb_builder.row(geo_btn, width=1)

keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)