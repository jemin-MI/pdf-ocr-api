from fastapi import  APIRouter
from src.api.v1.recipe_generator.route import upload_router


v1_router = APIRouter(prefix='/v1')
v1_router.include_router(upload_router, prefix="/pdf-upload", tags=["PDF Upload"])