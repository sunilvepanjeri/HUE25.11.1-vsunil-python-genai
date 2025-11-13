from fastapi import APIRouter
from . import frontend
from . import message



router = APIRouter()

router.include_router(frontend.router, prefix="/auth", tags=["frontend"])

router.include_router(message.router, prefix="/message", tags=["message"])
