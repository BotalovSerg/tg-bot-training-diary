from aiogram import Router

from .commands import router as commmand_router
from .users import router as users_router
from .training import router as train_router
from .admin import router as admin_router


def get_routers() -> list[Router]:
    return [
        commmand_router,
        users_router,
        train_router,
        admin_router,
    ]
