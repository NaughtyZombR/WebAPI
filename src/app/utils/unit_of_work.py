from app.db import async_session_maker
from app.repositories import *
from app.repositories.board import BoardsRepository
from app.repositories.board_column import BoardColumnsRepository


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.boards = BoardsRepository(self.session)
        self.board_columns = BoardColumnsRepository(self.session)
        self.tasks = TasksRepository(self.session)
        self.task_history = TaskHistoryRepository(self.session)

    async def __aexit__(self, *args):
        # await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
