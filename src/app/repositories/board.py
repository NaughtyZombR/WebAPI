from app.modules.boards.models import Board
from app.repositories._base_SQLAlchemy_repository import SQLAlchemyRepository


class BoardsRepository(SQLAlchemyRepository):
    model = Board
