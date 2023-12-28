from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import NoResultFound
from fastapi import status
from fastapi.responses import JSONResponse

from app.api.utis.dependencies import UOWDep
from app.api.utis.websockets import Notification, NotificationAction
from app.modules.tasks.schemas import TaskSchema, TaskSchemaCreate, TaskSchemaUpdate
from app.modules.users.fastapi_users_config import current_user
from app.modules.users.models import User
from app.services.boards import BoardsService
from app.services.tasks import TasksService

router = APIRouter(prefix="/columns/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskSchema)
async def create_task(uow: UOWDep, task_schema: TaskSchemaCreate, user: User = Depends(current_user)):
    task = await TasksService.create_task(uow, task_schema, user=user)
    # await Notification.notify_clients(f"Created the task '{task.title}'")
    await Notification.notify_clients_about_operations(entity=task, action=NotificationAction.created)
    return task


@router.get("/", response_model=List[TaskSchema])
async def read_tasks(uow: UOWDep, offset: int = 0, limit: int = 10):
    tasks = await TasksService.get_tasks(uow, offset=offset, limit=limit)
    return tasks


@router.get("/{task_id}", response_model=TaskSchema)
async def read_task(uow: UOWDep, task_id: int):
    try:
        task = await TasksService.get_task(uow, task_id)
        return task
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )


@router.get("/{task_id}/history", response_model=TaskSchema)
async def read_task_history(uow: UOWDep, task_id: int):
    task = await TasksService.get_task_histories(uow, task_id)
    return task


@router.patch("/{task_id}", response_model=TaskSchema)
async def update_task(uow: UOWDep, task_id: int, task_schema: TaskSchemaUpdate, user: User = Depends(current_user)):
    try:
        task = await TasksService.edit_task(uow, task_id, task_schema, user)
        # await Notification.notify_clients(f"Updated the task '{task.title}")
        await Notification.notify_clients_about_operations(entity=task, action=NotificationAction.updated)

        return task
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )


@router.delete("/{task_id}")
async def delete_task(uow: UOWDep, task_id: int, user: User = Depends(current_user)):
    try:
        task = await TasksService.get_task(uow, task_id)
        await TasksService().delete_task(uow, task_id)

        # await Notification.notify_clients(f"Deleted the task (ID: '{task_id})'")
        await Notification.notify_clients_about_operations(entity=task, action=NotificationAction.deleted)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"product": "Task deleted successfully"},
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )


@router.get("/column/{board_column_id}", response_model=List[TaskSchema])
async def read_specific_board_column(uow: UOWDep, board_column_id: int):
    try:
        board_column = await BoardsService.get_board_column(uow, board_column_id)
        tasks = board_column.tasks
        return tasks if tasks is not None else list()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )

