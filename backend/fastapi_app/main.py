from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Request
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from fastapi.middleware.wsgi import WSGIMiddleware
from django.core.wsgi import get_wsgi_application
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

app = FastAPI()
templates = Jinja2Templates(directory="templates")

django_app = get_wsgi_application()
app.mount("/django", WSGIMiddleware(django_app))


@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.get("/api")
async def api_root(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"message": "Hello from FastAPI with DB!"}


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/chat/{chat_id}")
async def websocket_chat(websocket: WebSocket, chat_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Chat {chat_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
