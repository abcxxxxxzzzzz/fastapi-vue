from typing import List
from fastapi import WebSocket


#  用于管理websocket的连接
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_json(self,data,websocket: WebSocket):
        await websocket.send_json(data)

    # 给所有连接发送文本
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

WebSocketManager = ConnectionManager()
