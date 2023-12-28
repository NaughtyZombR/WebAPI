from app.modules.boards.models import BoardColumn
from app.repositories._base_SQLAlchemy_repository import SQLAlchemyRepository


class BoardColumnsRepository(SQLAlchemyRepository):
    model = BoardColumn
