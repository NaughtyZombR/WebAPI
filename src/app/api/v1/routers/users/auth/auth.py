from fastapi import APIRouter

from app.modules.users.auth.auth_config import auth_backend
from app.modules.users.schemas import UserCreate, UserRead
from app.modules.users.fastapi_users_config import fastapi_users

# Auth Router

router = APIRouter(tags=["Auth"])

router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
router.include_router(fastapi_users.get_auth_router(auth_backend))
