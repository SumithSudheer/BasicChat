# app/connection_manager.py

from typing import Dict, List
from fastapi import WebSocket

# Stores clients in-memory, grouped by room_id
clients: Dict[str, WebSocket] = {}

def add_client(room_id: str, websocket: WebSocket):
    if room_id not in clients:
        clients[room_id] = None
    clients[room_id]=websocket
    print(clients,"sssssssssssssssssssssss",flush=True)
    
def remove_client(room_id: str, websocket: WebSocket):
    if room_id in clients and websocket in clients[room_id]:
        clients[room_id]=None
        if not clients[room_id]:  # Clean up if empty
            del clients[room_id]

def get_clients(room_id: str) -> List[WebSocket]:
    return clients.get(room_id, None)
