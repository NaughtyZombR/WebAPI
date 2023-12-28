# from typing import List
#
# from app.modules.boards.models import BoardColumn
# from app.modules.boards.schemas import BoardSColumnSchemaCreate, BoardColumnSchemaUpdate
# from app.utils.unit_of_work import UnitOfWork
#
#
# class BoardColumnsService:
#     @staticmethod
#     async def create_board_column(uow: UnitOfWork, board_column_schema: BoardColumnSchemaCreate) -> BoardColumn:
#         async with uow:
#             board_column = await uow.board_columns.create(board_column_schema)
#             await uow.commit()
#             return board_column
#
#     @staticmethod
#     async def get_board_column(uow: UnitOfWork, board_column_id: int) -> BoardColumn:
#         async with uow:
#             board_column = await uow.board_columns.get(board_column_id)
#             return board_column
#
#     @staticmethod
#     async def get_board_columns(uow: UnitOfWork, offset: int = 0, limit: int | None = None) -> List[BoardColumn]:
#         async with uow:
#             board_columns = await uow.board_columns.get_all(offset=offset, limit=limit)
#             return board_columns
#
#     @staticmethod
#     async def edit_board_column(uow: UnitOfWork, board_column_id: int, board_column_schema: BoardColumnSchemaUpdate) -> BoardColumn:
#         async with uow:
#             board_column = await uow.board_columns.edit(board_column_id, board_column_schema)
#
#             await uow.commit()
#             return board_column
#
#     @staticmethod
#     async def delete_board_column(uow: UnitOfWork, board_column_id: int):
#         async with uow:
#             await uow.board_columns.delete(board_column_id)
#             await uow.commit()
#
