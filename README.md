# 🚀 FastAPI WebSocket Chat App with Redis Pub/Sub

This is a FastAPI-based real-time chat application using **WebSockets** and **Redis Pub/Sub**. Messages are routed from one user to another using Redis channels, enabling real-time communication even across multiple workers or instances.

---

## 📦 Features

- WebSocket connections per user.
- JSON message format with `to`, `from`, and `message` fields.
- Redis Pub/Sub for message routing between users.
- Dockerized for easy deployment.
- Scalable via Redis broker (supports future scaling with multiple instances).

---

## 🔧 Project Structure




<pre>
.
├── app
│   ├── auth.py
│   ├── connection_manager.py
│   ├── db.py
│   ├── main.py
│   ├── models.py
│   ├── redis.py
│   ├── schema.py
│   └── websocket.py
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
 </pre>



---

## 🚀 Getting Started

### 1. Clone the repository

<pre>
git clone https://github.com/yourusername/fastapi-ws-redis.git
</pre>


Run the app using Docker Compose
<pre>
docker-compose up --build
</pre>
The FastAPI server will be available at:
<pre>
📡 http://localhost:8000
</pre>
WebSocket endpoint:
<pre>
📨 ws://localhost:8000/ws/{user_id}
</pre>
<pre>
🔁 ws://localhost:8000/ws/redis/{user_id} 
</pre>
for Redis Pub/Sub handler.




Example WebSocket Message Body
Send this message via WebSocket from user 11:

<pre>
{
  "to": "1",
  "from": "11",
  "message": "hello1"
}
</pre>

If user 1 is connected, they'll receive:

<pre>

{
  "from": "11",
  "message": "hello1"
}


</pre>


🔌 API Endpoints
<pre>
Method	Endpoint	Description
WS	/ws/{user_id}	Basic user WebSocket
WS	/ws/redis/{user_id}	Redis-based WebSocket routing
</pre>


---

Let me know if you'd like to include:
- Redis Streams instead of Pub/Sub
- Database storage for messages
- JWT-authentication in WebSocket URLs

And I can update this `README.md` or help you build those features.