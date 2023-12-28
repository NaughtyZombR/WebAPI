from fastapi import APIRouter
from .board import router as boards_router
from .board_column import router as board_columns_router
from .task import router as tasks_router


router = APIRouter(
    prefix="/boards",
)

router.include_router(boards_router)
router.include_router(board_columns_router)
router.include_router(tasks_router)
