from fastapi import APIRouter

from src.main.routes.ws_routes import ws_router

router = APIRouter(
  prefix="/api",
)

router.include_router(ws_router)

