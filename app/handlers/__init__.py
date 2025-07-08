__all__ = ("router", )

from aiogram import Router
from app.handlers.message import router as message_router
from app.handlers.callback import router as callback_router

router = Router()
router.include_routers(callback_router, message_router)