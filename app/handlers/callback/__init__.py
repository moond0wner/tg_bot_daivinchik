__all__ = ("router", )

from aiogram import Router

from app.handlers.callback.create_profile import router as router_create_profile
from app.handlers.callback.get_profile import router as router_get_profile
from app.handlers.callback.scroll_profiles import router as router_scroll_profiles
from app.handlers.callback.start import router as router_start
from app.handlers.callback.send_problem import router as router_send_problem

router = Router()
router.include_routers(router_get_profile, router_create_profile, router_scroll_profiles, router_start, router_send_problem)