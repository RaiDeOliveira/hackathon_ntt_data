from fastapi import APIRouter

from src.main.routes import ws_routes
from src.main.routes import chat_routes

router = APIRouter(
  prefix="/api",
)

router.include_router(ws_routes.router)
router.include_router(chat_routes.router)

