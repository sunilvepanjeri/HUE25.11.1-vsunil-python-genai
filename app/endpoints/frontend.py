from fastapi import APIRouter
from app.helper import load_users, save_users
from pydantic import BaseModel
from loguru import logger

router = APIRouter()

class User(BaseModel):
    Email: str
    password: str

@router.post("/login")
async def login(user: User):
    users = await load_users()
    if user.Email not in users or users[user.Email]["password"] != user.password:
        logger.error(f"Username {user.Email} doesn't exist")
        return {"value": False, "message": "Invalid credentials"}
    logger.debug(f"Username {user.Email} logged in")
    return {"value": True, "message": "Login successful"}

@router.post("/signup")
async def signup(user: User):
    users = await load_users()
    if user.Email in users:
        logger.error(f"Username {user.Email} already exists")
        return {"value": False, "message": "User already exists"}
    users[user.Email] = {"password": user.password}
    await save_users(users)
    logger.debug(f"Username {user.Email} Signed up")
    return {"value": True, "message": "Signup successful Login to Proceed"}