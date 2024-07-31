from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Account


async def get_user_by_id(session: AsyncSession, user_id: int) -> Account | None:
    stmt = select(Account).where(Account.telegram_id == user_id)
    return await session.scalar(stmt)


async def create_user(session: AsyncSession, user_id: int, username: str) -> None:
    existing_user = await get_user_by_id(session, user_id)
    if existing_user is not None:
        return
    user = Account(
        telegram_id=user_id,
        username=username,
    )
    session.add(user)
    await session.commit()


async def update_profile_user(session: AsyncSession, user_id: int, data: dict) -> None:
    query = (
        update(Account)
        .where(Account.telegram_id == user_id)
        .values(
            first_name=data["first_name"],
            last_name=data["last_name"],
            age=data["age"],
            bio=data["bio"],
        )
    )
    await session.execute(query)
    await session.commit()
