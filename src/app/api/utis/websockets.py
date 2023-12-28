import json
from enum import Enum
from typing import Optional

from app.db import Base as ModelBase
from fastapi import APIRouter, WebSocket

from app.modules.boards.models import Board, BoardColumn
from app.modules.tasks.models import Task

router = APIRouter()


# WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()





class NotificationAction(Enum):
    created = "created"
    updated = "updated"
    deleted = "deleted"



class Notification:
    @staticmethod
    async def notify_clients(message: str):
        for connection in manager.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def notify_clients_about_operations(entity: ModelBase | str, action: NotificationAction, entity_data: Optional[dict] = None, entity_id: Optional[int] = None):
        constructor = Notification.NotifyConstructor(entity, action, entity_data, entity_id)
        result = constructor.generate_json()
        await Notification.notify_clients(result)

    class NotifyConstructor:
        entity: ModelBase | str
        action: NotificationAction
        entity_data: Optional[dict] = None
        entity_id: Optional[int] = None

        def __init__(self, entity: ModelBase | str, action: NotificationAction, entity_data: Optional[dict] = None, entity_id: Optional[int] = None):
            self.entity = entity
            self.action = action
            self.entity_data = entity_data
            self.entity_id = entity_id

        def generate_json(self):
            data = self._parse_entity()
            entity_class = self.entity.__class__.__name__.lower() if issubclass(self.entity.__class__, ModelBase) else self.entity
            return json.dumps({"type": self.action.value, "entity": entity_class, "data": data})

        def _parse_entity(self):
            if isinstance(self.entity, Task):
                return self._create_notify_task_json()
            elif isinstance(self.entity, Board):
                return self._create_notify_board_json()
            elif isinstance(self.entity, BoardColumn):
                return self._create_notify_board_column_json()
            else:
                if issubclass(self.entity, ModelBase):
                    return {"id": self.entity.id}
                else:
                    return {"id": self.entity_id}

        def _create_notify_task_json(self):
            return {"id": self.entity.id,
                               "title": self.entity.title,
                               "author_id": self.entity.author_id,
                               "assignee_id": self.entity.assignee_id}

        def _create_notify_board_json(self):
            return {"id": self.entity.id,
                               "title": self.entity.title,
                               "owner": {"id": self.entity.owner_id, "username": self.entity.owner.username}}

        def _create_notify_board_column_json(self):
            return {"id": self.entity.id,
                               "title": self.entity.title,
                               "board": {"id": self.entity.board_id, "title": self.entity.board.title}}

