from app.connection_manager import get_clients
import redis.asyncio as redis

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)
PUBSUB_PREFIX = "user:" 

async def redis_subscriber(user_id: str):
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(PUBSUB_PREFIX + user_id)

    async for message in pubsub.listen():
        if message['type'] == 'message':
            try:
                # Forward the message to the correct WebSocket connection
                websocket = get_clients(user_id)
                if websocket:
                    await websocket.send_text(message['data'])
            except:
                pass  # WebSocket might have disconnected

# ADD THIS FUNCTION IF YOU WANT TO PUBLISH MESSAGES TO REDIS
async def publish_message(room_id: str, message: str):
    await redis_client.publish(room_id, message)
    # print(r.get(room_id))
    # await redis_subscriber()
