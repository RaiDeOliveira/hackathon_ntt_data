from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import logging

from src.models.settings.connection import db_connection_handler
from src.config.settings import config
from src.service.mqtt_service import start_mqtt
from src.websocket.websocket_manager import WebSocketManager
from src.main.server.server import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

server_config = config["api"]
websocket_manager = WebSocketManager()

db_connection_handler.connect_to_db()

app = FastAPI(
  debug=bool(server_config["debug"]),
  title=server_config["title"],
)

@app.on_event("startup")
def on_startup() -> None:
  logger.info("Starting MQTT...")
  start_mqtt()
  
if server_config["debug"]:
  origins = ["*"]
else:
  origins = [
      str(origin).strip(",") for origin in server_config["ORIGINS"]
  ]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
  uvicorn.run(
    app,
    host=server_config["host"],
    port=server_config["port"],
    reload=server_config["reload"]
  )