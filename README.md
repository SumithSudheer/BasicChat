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

