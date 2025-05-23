from fastapi import FastAPI
from app.websocket import websocket_endpoint
from fastapi.middleware.cors import CORSMiddleware
from fastapi import WebSocket, WebSocketDisconnect
from app.redis import publish_message
from app.connection_manager import add_client, remove_client, get_clients
from .db import Base, engine
from .models import User
from .auth import router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_api_websocket_route("/ws/{room_id}", websocket_endpoint)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

app.include_router(router, prefix="/api/auth", tags=["Auth"])

@app.get("/")
async def get():
    print("hererererer")
    return {"test":"Ok"}

# @app.websocket("/ws/{room_id}")
