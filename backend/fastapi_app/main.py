from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.connections.remove(ws)

    async def broadcast(self, message: str):
        for conn in self.connections:
            await conn.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{chat_id}")
async def websocket_endpoint(ws: WebSocket, chat_id: int):
    await manager.connect(ws)
    try:
        while True:
            data = await ws.receive_text()
            await manager.broadcast(f"Chat {chat_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(ws)


@app.websocket("/ws/{room_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message from {room_name}: {data}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

@app.get("/")
async def root(db: AsyncSession = Depends(get_db)):
    # Можно сделать запрос к БД тут, например:
    result = await db.execute("SELECT 1")
    return {"message": "Hello from FastAPI with DB!"}