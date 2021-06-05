from collections import defaultdict
from typing import DefaultDict, List, Dict

from fastapi import WebSocket
import aioredis

class SessionHub:
    def __init__(self):
        self.active_sessions: DefaultDict[str, DefaultDict()] = {}

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


active_sessions = defaultdict(dict)
