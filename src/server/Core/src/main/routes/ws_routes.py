from fastapi import APIRouter, WebSocket
import logging
from src.websocket.websocket_manager import WebSocketManager

router = APIRouter(
  prefix="/ws",
  tags=["WebSocket"]
)

websocket_manager = WebSocketManager()

@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
  await websocket_manager.connect(websocket)
  try:
    while True:
      await websocket.receive_text()
  except Exception as e:
    logging.exception(f"WebSocket error: {str(e)}")
  finally:
    websocket_manager.disconnect(websocket)
