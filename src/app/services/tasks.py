from typing import List

from app.modules.tasks.models import Task, TaskHistory
from app.modules.tasks.schemas import (
    TaskHistorySchemaCreate,
    TaskSchemaCreate,
    TaskSchemaUpdate,
)
from app.modules.users.models import User
from app.utils.unit_of_work import UnitOfWork


class TasksService:
    @staticmethod
    async def create_task(uow: UnitOfWork, task_schema: TaskSchemaCreate, user: User) -> Task:
        async with uow:
            task_data = task_schema.model_dump()
            task_data["author_id"] = user.id
            task = await uow.tasks.create(task_data)
            await uow.commit()
            return task

    @staticmethod
    async def get_task(uow: UnitOfWork, task_id: int) -> Task:
        async with uow:
            task = await uow.tasks.get(task_id)
            return task

    @staticmethod
    async def get_tasks(
        uow: UnitOfWork, offset: int = 0, limit: int | None = None
    ) -> List[Task]:
        async with uow:
            tasks = await uow.tasks.get_all(offset=offset, limit=limit)
            return tasks

    @staticmethod
    async def edit_task(
        uow: UnitOfWork, task_id: int, task_schema: TaskSchemaUpdate, user: User
    ) -> Task:
        async with uow:
            task = await uow.tasks.edit(task_id, task_schema)

            task_history_schema = TaskHistorySchemaCreate(
                task_id=task_id,
                board_column_id=task.board_column_id,
                previous_assignee_id=task.assignee_id,
                new_assignee_id=task.assignee_id,
                editor_id=user.id
            )

            await uow.task_history.create(task_history_schema)

            await uow.commit()
            return task

    @staticmethod
    async def delete_task(uow: UnitOfWork, task_id: int):
        async with uow:
            await uow.tasks.delete(task_id)
            await uow.commit()

    @staticmethod
    async def get_task_histories(uow: UnitOfWork, task_id: int) -> TaskHistory:
        async with uow:
            task = await uow.tasks.get(task_id)
            task_history = task.task_histories
            return task_history
