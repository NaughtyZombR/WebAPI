from fastapi import APIRouter

from app.api.v1.routers.users import router as users_router
from app.api.v1.routers.boards import router as tasks_router

router = APIRouter(prefix="/v1")

router.include_router(users_router)
router.include_router(tasks_router)
