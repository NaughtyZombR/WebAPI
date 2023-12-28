from typing import List

from app.modules.boards.models import Board, BoardColumn
from app.modules.boards.schemas import (
    BoardSchemaCreate,
    BoardSchemaUpdate,
    BoardColumnSchemaCreate,
    BoardColumnSchemaUpdate,
)
from app.modules.users.models import User
from app.utils.unit_of_work import UnitOfWork


class BoardsService:
    # ~~ Board ~~
    @staticmethod
    async def create_board(uow: UnitOfWork, board_schema: BoardSchemaCreate, user: User) -> Board:
        async with uow:
            board_data = board_schema.model_dump()
            board_data["owner_id"] = user.id
            board = await uow.boards.create(board_data)
            await uow.commit()
            return board

    @staticmethod
    async def get_board(uow: UnitOfWork, board_id: int) -> Board:
        async with uow:
            board = await uow.boards.get(board_id)
            return board

    @staticmethod
    async def get_boards(
        uow: UnitOfWork, offset: int = 0, limit: int | None = None
    ) -> List[Board]:
        async with uow:
            boards = await uow.boards.get_all(offset=offset, limit=limit)
            return boards

    @staticmethod
    async def edit_board(
        uow: UnitOfWork, board_id: int, board_schema: BoardSchemaUpdate
    ) -> Board:
        async with uow:
            board = await uow.boards.edit(board_id, board_schema)

            await uow.commit()
            return board

    @staticmethod
    async def delete_board(uow: UnitOfWork, board_id: int):
        async with uow:
            await uow.boards.delete(board_id)
            await uow.commit()

    # ~~ Board Column ~~
    @staticmethod
    async def create_board_column(
        uow: UnitOfWork, board_column_schema: BoardColumnSchemaCreate
    ) -> BoardColumn:
        async with uow:
            board_column = await uow.board_columns.create(board_column_schema)
            await uow.commit()
            return board_column

    @staticmethod
    async def get_board_column(uow: UnitOfWork, board_column_id: int) -> BoardColumn:
        async with uow:
            board_column = await uow.board_columns.get(board_column_id)
            return board_column

    @staticmethod
    async def get_board_columns(
        uow: UnitOfWork, offset: int = 0, limit: int | None = None
    ) -> List[BoardColumn]:
        async with uow:
            board_columns = await uow.board_columns.get_all(offset=offset, limit=limit)
            return board_columns

    @staticmethod
    async def edit_board_column(
        uow: UnitOfWork,
        board_column_id: int,
        board_column_schema: BoardColumnSchemaUpdate,
    ) -> BoardColumn:
        async with uow:
            board_column = await uow.board_columns.edit(
                board_column_id, board_column_schema
            )

            await uow.commit()
            return board_column

    @staticmethod
    async def delete_board_column(uow: UnitOfWork, board_column_id: int):
        async with uow:
            await uow.board_columns.delete(board_column_id)
            await uow.commit()
