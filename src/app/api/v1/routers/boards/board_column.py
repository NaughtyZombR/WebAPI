from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from fastapi import status
from fastapi.responses import JSONResponse

from app.api.utis.dependencies import UOWDep
from app.api.utis.websockets import Notification, NotificationAction
from app.modules.boards.schemas import (
    BoardColumnSchema,
    BoardColumnSchemaCreate,
    BoardColumnSchemaUpdate,
)
from app.services.boards import BoardsService

router = APIRouter(prefix="/columns", tags=["Board-Columns"])


@router.post("/", response_model=BoardColumnSchema)
async def create_board_column(
    uow: UOWDep, board_column_schema: BoardColumnSchemaCreate
):
    board_column = await BoardsService.create_board_column(uow, board_column_schema)
    # await Notification.notify_clients(f"Created the board_column '{board_column.title}'")
    await Notification.notify_clients_about_operations(entity=board_column, action=NotificationAction.created)
    return board_column


@router.get("/", response_model=List[BoardColumnSchema])
async def read_board_columns(uow: UOWDep, offset: int = 0, limit: int = 10):
    board_columns = await BoardsService.get_board_columns(
        uow, offset=offset, limit=limit
    )
    return board_columns


@router.get("/{board_column_id}", response_model=BoardColumnSchema)
async def read_board_column(uow: UOWDep, board_column_id: int):
    try:
        board_column = await BoardsService.get_board_column(uow, board_column_id)
        return board_column
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board_column not found"
        )


@router.patch("/{board_column_id}", response_model=BoardColumnSchema)
async def update_board_column(
    uow: UOWDep, board_column_id: int, board_column_schema: BoardColumnSchemaUpdate
):
    try:
        board_column = await BoardsService.edit_board_column(
            uow, board_column_id, board_column_schema
        )
        # await Notification.notify_clients(f"Updated the board_column '{board_column.title}")
        await Notification.notify_clients_about_operations(entity=board_column, action=NotificationAction.updated)
        return board_column
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board_column not found"
        )


@router.delete("/{board_column_id}")
async def delete_board_column(uow: UOWDep, board_column_id: int):
    try:
        board_column = await BoardsService.get_board_column(uow, board_column_id)
        await BoardsService().delete_board_column(uow, board_column_id)

        # await Notification.notify_clients(f"Deleted the board_column (ID: '{board_column_id})'")
        await Notification.notify_clients_about_operations(entity=board_column, action=NotificationAction.deleted)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"product": "Board_column deleted successfully"},
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board_column not found"
        )


@router.get("/board/{board_id}", response_model=List[BoardColumnSchema])
async def read_specific_board_column(uow: UOWDep, board_id: int):
    try:
        board = await BoardsService.get_board(uow, board_id)
        board_column = board.columns
        return board_column if board_column is not None else list()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )