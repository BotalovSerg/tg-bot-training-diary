from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from bot.database.models import Account, CategoryScheme, Scheme


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


async def test_connection(session: AsyncSession):
    """
    Проверка соединения с СУБД
    :param session: объект AsyncSession
    """
    stmt = select(1)
    return await session.scalar(stmt)


async def create_category(session: AsyncSession, title: str) -> None:
    category = CategoryScheme(title=title)
    session.add(category)
    await session.commit()


async def get_all_category(session: AsyncSession) -> list[CategoryScheme]:
    stmt = select(CategoryScheme).order_by(CategoryScheme.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_all_scheme_on_category(
    session: AsyncSession, cat_id: int
) -> list[Scheme]:
    stmt = select(Scheme).where(Scheme.category_id == cat_id).order_by(Scheme.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_scheme_by_id(session: AsyncSession, scheme_id: int) -> Scheme:
    stmt = (
        select(Scheme)
        .where(Scheme.id == scheme_id)
        .options(joinedload(Scheme.category))
    )
    result = await session.scalar(stmt)

    return result
