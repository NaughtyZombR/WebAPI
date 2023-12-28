from app.modules.users.models import User
from app.repositories._base_SQLAlchemy_repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = User
