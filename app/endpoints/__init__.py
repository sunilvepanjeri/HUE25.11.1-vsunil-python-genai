from fastapi import APIRouter
from . import frontend



router = APIRouter()

router.include_router(frontend.router, prefix="/auth", tags=["frontend"])
