__all__ = ("router", )

from aiogram import Router

from app.handlers.message.create_profile import router as router_create_profile
from app.handlers.message.start import router as router_start
from app.handlers.message.send_problem import router as router_send_problem

router = Router()
router.include_routers(router_start, router_create_profile, router_send_problem)