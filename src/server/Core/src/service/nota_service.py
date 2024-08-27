from src.models.repository.sensor_repository import SensorRepository
from src.websocket.websocket_client import get_websocket_client

class NotaService:
  def __init__(self):
    self.__sensor_repository = SensorRepository()
    self.__ws_client = get_websocket_client()
  
  async def get_dados_db(self):
    return self.__sensor_repository.get_all_sensors()
  
  async def ibutg_generate(self):
    pass
  
  async def dados_camera_ws(self):
    return self.__ws_client.get_last_message()