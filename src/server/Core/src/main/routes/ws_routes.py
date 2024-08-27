import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging
import json

from src.websocket.websocket_manager import websocket_manager
from src.models.repository.sensor_repository import SensorRepository
from src.service.nota_service import NotaService
from src.models.repository.quality_model_repository import QualityRepository
from src.service.quality_model_service import calcule_and_save_quality_data


router = APIRouter(
  prefix="/ws",
  tags=["WebSocket"]
)

sensor_repository = SensorRepository()
nota_service = NotaService()
quality_repository = QualityRepository()

@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
          data = await websocket.receive_text()
          await websocket_manager.broadcast(data)
    except WebSocketDisconnect:
        logging.info("Client disconnected")
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
      await websocket_manager.broadcast(sensors_json)
      await asyncio.sleep(5)
  except WebSocketDisconnect:
    logging.info("Client disconnected")
  except Exception as e:
    logging.exception(f"WebSocket error: {str(e)}")
  finally:
    websocket_manager.disconnect(websocket)

@router.websocket("/Quality")
async def nota_websocket_endpoint(websocket: WebSocket):
  await websocket_manager.connect(websocket)
  try:
    while True:
      
      calcule_and_save_quality_data()
      quality = quality_repository.get_all_quality()
      quality_json = json.dumps(quality)
      await websocket_manager.broadcast(quality_json)
      await asyncio.sleep(5)
  except WebSocketDisconnect:
    logging.info("Client disconnected")
  except Exception as e:
    logging.exception(f"WebSocket error: {str(e)}")
  finally:
    websocket_manager.disconnect(websocket)