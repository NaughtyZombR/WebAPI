from fastapi.websockets import WebSocket, WebSocketDisconnect

from app.admin_panel.apanel import AdminPanel
from app.api.utis.websockets import manager
from app.api import router
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.db import engine

# Templates
templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title="Упрощённый аналог Trello",
    summary="WebSocket Chat + Notifications of CRUD operations!",
    description="""
    Данный проект представляет из себя небольшую копию Trello — онлайн-система управления проектами. 
    Реализована система регистрации, авторизации, аутентификации пользователей. 
    
    Методы, помеченные замком, могут быть выполнены в Swagger UI документации только в том случае, 
    если будет осуществлён вход в зарегистрированный аккаунт, посредством авторизации через кнопку `Authorize` 
    в правом верхнем углу страницы, где username - почта, а password - пароль. 
    
    При успешном входе будет предоставлен JWT токен, который будет записан в куки браузера.
    Была сделана Админ-Панель, располагающаяся по адресу `/admin`. Для входа нужен аккаунт superuser'а. 
    Таковым является 'admin@trello.com' с паролем 'root'.
    
    Поскольку frontend часть не обязательна (а я как раз в ней не силён), я пропустил этот этап на половине, 
    можете потыкаться, но сильно чего-то многого не ожидайте, это просто макет. 
    Времени нет на создание того, над чем я не силён. 
    
    По корневому пути оставил немного изменённый чат с документации фреймворка, который мы разбирали на лекциях. 
    Если бы и делал фронт часть, то я его бы всё равно включил в итоговый вариант, как некую возможность общения с 
    "коллегами" внутри сайта. Ответы, отправляемыми WebSocket'ом клиенту были типизированы в JSON формат, для 
    разделения логики как уведомлений, так и общения в чате. Для тестирования WebSocket'а перейдите по корневому пути, 
    или воспользуйтесь сторонним клиентом и подключитесь по пути '/ws/{client_name}'.
    """,
    version="0.0.1",
)


@app.on_event("startup")
async def startup():
    # Include routers
    app.include_router(router)

    # Initialize AdminPanel
    AdminPanel(app, engine)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    server_urn = f"{request.scope.get('server')[0]}:{request.scope.get('server')[1]}"
    return templates.TemplateResponse(
        "general.html", {"request": request, "server_urn": server_urn}
    )


@app.websocket("/ws/{client_name}")
async def websocket_endpoint(websocket: WebSocket, client_name: str):
    await manager.connect(websocket)
    await manager.broadcast(f"Client #{client_name} joined the chat")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_name} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_name} left the chat")
