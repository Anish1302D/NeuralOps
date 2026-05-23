from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import asyncio
from typing import List

router = APIRouter(prefix="/stream", tags=["websocket"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.broadcast({"type": "system", "message": "[WS] Client connected to NeuralOps stream."})

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except RuntimeError:
                pass

manager = ConnectionManager()

@router.websocket("/events")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo input back as a user command
            await manager.broadcast({"type": "user_command", "message": f"> {data}"})
            
            # Simulate a quick response sequence
            await asyncio.sleep(0.5)
            await manager.broadcast({"type": "info", "message": "[SYSTEM] Analyzing command..."})
            await asyncio.sleep(1)
            await manager.broadcast({"type": "agent", "message": "[AGENT_ROUTER] Spawning execution workflow..."})
            await asyncio.sleep(1.5)
            await manager.broadcast({"type": "success", "message": "[SUCCESS] Command execution completed."})

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({"type": "system", "message": "[WS] Client disconnected."})
