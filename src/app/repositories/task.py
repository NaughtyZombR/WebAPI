from app.modules.tasks.models import Task
from app.repositories._base_SQLAlchemy_repository import SQLAlchemyRepository


class TasksRepository(SQLAlchemyRepository):
    model = Task
