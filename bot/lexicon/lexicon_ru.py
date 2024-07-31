from typing import TypedDict, Dict


class LexiconRuMenuDTO(TypedDict):
    main_menu: Dict[str, str]


class LexiconRuDTO(TypedDict):
    command: Dict[str, str]


LEXICON_MENU = LexiconRuMenuDTO(
    main_menu={
        "/help": "Список доступных команд",
        "/settings": "настройки бота",
        "/contact": "Информация для связи 😀",
    }
)


LEXICON_COMMANDS = LexiconRuDTO(
    commands={
        # ----command /start ----
        "/start": "<b>Здавствуйте!</b>\n"
        "Рад приветсвовать вас в дневнике тренировок. Начнем вести ваши спортивные достижения?\n"
        "Чтобы посмотреть список моих возможностей, нажми /help",
        # ----command /help ----
        "/help": "<b>Описание команд:\n\n</b>"
        "/all_workout - Список всех тренировок\n"
        "/add_workout - Добавить тренировку\n\n"
        "/exercises - Список упражнений\n"
        "/add_exercise - Добавить свое упражнение\n\n"
        "/profile - Профиль\n",
    }
)
