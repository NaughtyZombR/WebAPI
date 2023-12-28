from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from config import get_settings


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=get_settings().secret_key_jwt, lifetime_seconds=None
    )  # lifetime_seconds=4 * 60 * 60)


bearer_transport = BearerTransport(tokenUrl="/api/v1/users/auth/login")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
