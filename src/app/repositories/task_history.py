from app.modules.tasks.models import TaskHistory
from app.repositories._base_SQLAlchemy_repository import SQLAlchemyRepository


class TaskHistoryRepository(SQLAlchemyRepository):
    model = TaskHistory
