from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

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
