from typing import List

# from jwt import PyJWTError
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import User, Message
from .schema import MessageOut, UserCreate, TokenResponse, UserOut
from jose import jwt
from datetime import datetime, timedelta
from sqlalchemy import asc

router = APIRouter()
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created"}

@router.post("/login", response_model=TokenResponse)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": user.username,"user_id":db_user.id})
    return TokenResponse(access_token=token)


@router.get("/users", response_model=List[UserOut])
def user_list( db: Session = Depends(get_db)):
    db_user = db.query(User).filter()
    
    return db_user


@router.get("/me", response_model=dict)
def user_list(request:Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    token = auth_header.split(" ")[1]
    print(token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token missing user_id")
        return {"user_id":user_id}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Token is invalid")

    token = db.query(User).filter()
    jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
    return db_user



@router.get("/messages/{user_id}/{sender_id}", response_model=List[MessageOut])
def get_messages(user_id: int, sender_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message)\
        .filter(Message.sender_id == sender_id, Message.receiver_id == user_id)\
        .order_by(asc(Message.timestamp))\
        .all()
    
    return messages