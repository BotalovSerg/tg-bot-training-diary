from typing import TypedDict, Dict


class LexiconRuDTO(TypedDict):
    text: Dict[str, str]


LEXICON_MENU = LexiconRuDTO(
    text={
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


LEXICON_MESSAGE = LexiconRuDTO(
    text={
        "add_workout": "<b>Режим добавления тренировки.</b>\n"
        "1. Добавь место и описание тренировки (кардио, силовая, бег, турники и т.д.).\n"
        "Для выхода без сохранения отправить /reset",
        "save_training_plan": "2. Запишите план тернировки по пунктам, количество подходов.",
    }
)
