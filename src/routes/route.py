from fastapi import APIRouter
from src.routes.v1 import v1_router


route = APIRouter()
route.include_router(v1_router)