from fastapi import APIRouter

from app.api.v1.endpoints import asrs

v1_router = APIRouter()

v1_router.include_router(asrs.router, prefix="/main", tags=["main"])
