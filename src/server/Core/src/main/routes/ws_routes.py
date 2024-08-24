from fastapi import APIRouter, WebSocket
import logging
from src.websocket.websocket_manager import websocket_manager

router = APIRouter(
  prefix="/ws",
  tags=["WebSocket"]
)

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
