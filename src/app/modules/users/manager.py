from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin
from config import get_settings
from app.modules.users.models import User, get_user_db


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = get_settings().secret_reset_token
    verification_token_secret = get_settings().secret_verification_token


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
