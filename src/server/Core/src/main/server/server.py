from fastapi import APIRouter

from src.main.routes.temperature import router as temperature_router

router = APIRouter(
  prefix="/api",
)

router.include_router(temperature_router)

