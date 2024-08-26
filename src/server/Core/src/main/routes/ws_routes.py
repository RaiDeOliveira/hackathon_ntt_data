import asyncio
from fastapi import APIRouter, WebSocket
import logging
import json

from src.websocket.websocket_manager import websocket_manager
from src.models.repository.sensor_repository import SensorRepository

router = APIRouter(
  prefix="/ws",
  tags=["WebSocket"]
)

sensor_repository = SensorRepository()

@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
  await websocket_manager.connect(websocket)
  try:
    while True:
      data = await websocket.receive_text()
      await websocket_manager.send_personal_message(data, websocket)
  except Exception as e:
    logging.exception(f"WebSocket error: {str(e)}")
  finally:
    websocket_manager.disconnect(websocket)
    
@router.websocket("/sensor")
async def sensor_websocket_endpoint(websocket: WebSocket):
  await websocket_manager.connect(websocket)
  try:
    while True:
      sensors = sensor_repository.get_all_sensors()
      sensors_json = json.dumps(sensors)
      await websocket.send_text(sensors_json)
      await asyncio.sleep(5)
  except Exception as e:
    logging.exception(f"WebSocket error: {str(e)}")
  finally:
    websocket_manager.disconnect(websocket)