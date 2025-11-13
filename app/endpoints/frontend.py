from fastapi import APIRouter
from app.helper import load_users, save_users
from pydantic import BaseModel
from loguru import logger

router = APIRouter()

class User(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(user: User):
    users = await load_users()
    if user.username not in users or users[user.username]["password"] != user.password:
        logger.error(f"Username {user.username} doesn't exist")
        return {"value": False, "message": "Invalid credentials"}
    logger.debug(f"Username {user.username} logged in")
    return {"value": True, "message": "Login successful"}

@router.post("/signup")
async def signup(user: User):
    users = await load_users()
    if user.username in users:
        logger.error(f"Username {user.username} already exists")
        return {"value": False, "message": "User already exists"}
    users[user.username] = {"password": user.password}
    await save_users(users)
    logger.debug(f"Username {user.username} Signed up")
    return {"value": True, "message": "Signup successful Login to Proceed"}