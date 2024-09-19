from bot.database import Account


def get_profile_user(data_profile: Account) -> str:

    text = (
        f"👤\t<b>Profile</b>"
        "\n----------------------\n"
        f"<b>Username</b>: {data_profile.username}\n"
        f"<b>ID</b>: {data_profile.telegram_id or '-'}\n"
        f"<b>First name</b>: {data_profile.first_name or '-'}\n"
        f"<b>Last name</b>: {data_profile.last_name or '-'}\n"
        f"<b>Age</b>: {data_profile.age or '-'}\n"
        f"<b>BIO</b>: {data_profile.bio or '-'}\n"
    )

    return text
