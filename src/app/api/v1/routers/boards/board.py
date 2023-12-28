from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import NoResultFound
from fastapi import status
from fastapi.responses import JSONResponse

from app.api.utis.dependencies import UOWDep
from app.api.utis.websockets import Notification, NotificationAction
from app.modules.boards.schemas import BoardSchema, BoardSchemaCreate, BoardSchemaUpdate
from app.modules.users.fastapi_users_config import current_user
from app.modules.users.models import User
from app.services.boards import BoardsService

router = APIRouter(tags=["Boards"])


@router.post("/", response_model=BoardSchema)
async def create_board(uow: UOWDep, board_schema: BoardSchemaCreate, user: User = Depends(current_user)):
    board = await BoardsService.create_board(uow, board_schema, user=user)
    # await Notification.notify_clients(f"Created the board '{board.title}'")
    await Notification.notify_clients_about_operations(entity=board, action=NotificationAction.created)
    return board


@router.get("/", response_model=List[BoardSchema])
async def read_boards(uow: UOWDep, offset: int = 0, limit: int = 10):
    boards = await BoardsService.get_boards(uow, offset=offset, limit=limit)
    return boards


@router.get("/{board_id}", response_model=BoardSchema)
async def read_board(uow: UOWDep, board_id: int):
    try:
        board = await BoardsService.get_board(uow, board_id)
        return board
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )


@router.patch("/{board_id}", response_model=BoardSchema)
async def update_board(uow: UOWDep, board_id: int, board_schema: BoardSchemaUpdate, user: User = Depends(current_user)):
    try:
        board = await BoardsService.edit_board(uow, board_id, board_schema)
        await Notification.notify_clients_about_operations(entity=board, action=NotificationAction.updated)
        return board
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )


@router.delete("/{board_id}")
async def delete_board(uow: UOWDep, board_id: int, user: User = Depends(current_user)):
    try:
        board = await BoardsService.get_board(uow, board_id=board_id)

        await BoardsService().delete_board(uow, board_id)

        await Notification.notify_clients_about_operations(entity=board, action=NotificationAction.deleted)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"product": "Board deleted successfully"},
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )
