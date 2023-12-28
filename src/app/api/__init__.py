from fastapi import APIRouter

from app.api.utis import remove_trailing_slashes_from_routes
from app.api.v1 import router as router_v1

router = APIRouter(prefix="/api")

router.include_router(router_v1)

# Удаляем последний слэш в путях
router = remove_trailing_slashes_from_routes(router)
