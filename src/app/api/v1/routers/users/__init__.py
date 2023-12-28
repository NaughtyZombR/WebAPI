from fastapi import APIRouter
from .user_settings import router as settings_router
from .auth import router as auths_router

router = APIRouter(prefix="/users")

router.include_router(auths_router)
router.include_router(settings_router)
