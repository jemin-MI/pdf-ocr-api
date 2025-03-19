from fastapi import FastAPI
from src.routes.route import route as api_router

app = FastAPI(title="FastAPI PDF Processing API")

# Register all routers
app.include_router(api_router)



