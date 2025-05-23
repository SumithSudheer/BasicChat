import asyncio
from datetime import datetime
import json
from fastapi import WebSocket, WebSocketDisconnect
from app.redis import PUBSUB_PREFIX, publish_message, redis_subscriber
from app.connection_manager import add_client, remove_client, get_clients
import logging
from .models import Message
from .db import SessionLocal
from starlette.concurrency import run_in_threadpool

logger = logging.getLogger("uvicorn.error")

async def websocket_endpoint(websocket: WebSocket, room_id: str,token:str=None):
    logger.info("Connected to WebSocket")
    await websocket.accept()
    logger.info("here")
    add_client(room_id, websocket)
    
    

    try:
        while True:
            data = await websocket.receive_text()
            print("Received from client:", data,flush=True)
            payload = json.loads(data)
            to_user = payload.get("to")
            message = payload.get("message")
            sender_socket=get_clients(room_id=to_user)
            print(sender_socket,flush=True)
            await sender_socket.send_text(json.dumps({"to":to_user,"from":room_id,"message":message}))
            # if data:
            #     await websocket.send_text(data)
            # await run_in_threadpool(store_message, room_id, data, sender_id)
            await publish_message(room_id, data)
    except WebSocketDisconnect:
        remove_client(room_id, websocket)
        print("WebSocket disconnected",flush=True)
    except Exception as e:
        print(f"Error in WebSocket: {e}",flush=True)



async def websocket_endpoint_redis(websocket: WebSocket, room_id: str):
    await websocket.accept()
    add_client(room_id, websocket)

    # Start Redis subscriber in the background
    subscriber_task = asyncio.create_task(redis_subscriber(room_id))

    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            to_user = payload.get("to")
            message = payload.get("message")

            # Publish to recipient's Redis channel
            await publish_message(PUBSUB_PREFIX + to_user, json.dumps({
                "from": room_id,
                "message": message
            }))

    except WebSocketDisconnect:
        # del connected_users[user_id]
        subscriber_task.cancel()

def store_message(room_id: str, message: str, sender_id: int):
    db = SessionLocal()
    try:
        new_msg = Message(
            room_id=room_id,
            content=message,
            sender_id=sender_id,
            timestamp=datetime.utcnow()
        )
        db.add(new_msg)
        db.commit()
    except Exception as e:
        print("DB Error:", e)
        db.rollback()
    finally:
        db.close()