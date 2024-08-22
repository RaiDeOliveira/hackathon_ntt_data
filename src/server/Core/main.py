from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import logging

from src.config.settings import config
from src.service.mqtt_subscriber import start_mqtt
from src.main.server.server import router

server_config = config["api"]

app = FastAPI(
  debug=bool(server_config["debug"]),
  title=server_config["title"],
)

@app.on_event("startup")
async def startup_event():
  start_mqtt()

if server_config["debug"]:
    origins = ["*"]
else:
    origins = [
        str(origin).strip(",") for origin in server_config.ORIGINS
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)